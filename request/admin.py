from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django import forms
from django.conf import settings
from .models import VehiclePartRequest
from store.models import Shop, RequestHasShop
from store.whatsapp_service import whatsapp_service


class AssignShopsForm(forms.Form):
    """Form for assigning shops to requests"""
    shops = forms.ModelMultipleChoiceField(
        queryset=Shop.objects.filter(active=True).order_by('name'),
        widget=forms.SelectMultiple(attrs={'size': '10', 'style': 'width: 100%;'}),
        required=True,
        help_text="Select one or more shops to assign to the selected requests (hold Ctrl/Cmd to select multiple)"
    )
    custom_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        help_text="Optional custom message to add (request details will be automatically included)"
    )
    send_whatsapp = forms.BooleanField(
        required=False,
        initial=False,
        label="Send WhatsApp message to shops",
        help_text=""
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        whatsapp_enabled = getattr(settings, 'TWILIO_WHATSAPP_ENABLED', False)
        has_credentials = bool(
            getattr(settings, 'TWILIO_ACCOUNT_SID', '') and 
            getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        )
        
        if whatsapp_enabled and has_credentials:
            self.fields['send_whatsapp'].help_text = (
                "Send the request details via WhatsApp to selected shops "
                "(requires valid phone numbers in E.164 format)"
            )
        else:
            # Disable the field if WhatsApp is not configured
            self.fields['send_whatsapp'].help_text = (
                "⚠️ WhatsApp messaging is not configured. "
                "Please set TWILIO_WHATSAPP_ENABLED=True and provide Twilio credentials in your .env file"
            )
            # Still show the checkbox but it won't do anything if not configured


@admin.register(VehiclePartRequest)
class VehiclePartRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for VehiclePartRequest model
    """
    list_display = [
        'id', 'user', 'part_name', 
        'status', 'created_at'
    ]
    list_filter = [
        'vehicle_type', 'status', 'vehicle_year', 'created_at'
    ]
    search_fields = [
        'vehicle_model', 'part_name', 'part_number', 
        'user__email', 'user__first_name', 'user__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    actions = ['assign_shops_action']
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('vehicle_type', 'vehicle_model', 'vehicle_year', 'vehicle_image')
        }),
        ('Part Information', {
            'fields': ('part_name', 'part_number', 'part_image', 'part_video')
        }),
        ('Request Details', {
            'fields': ('user', 'description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def vehicle_display(self, obj):
        return obj.vehicle_display
    vehicle_display.short_description = 'Vehicle'
    
    def assign_shops_action(self, request, queryset):
        """
        Admin action to assign shops to selected requests
        """
        # Check if this is a form submission from the intermediate page
        if 'apply' in request.POST:
            form = AssignShopsForm(request.POST)
            if form.is_valid():
                # Get selected request IDs from POST data
                selected_ids = request.POST.getlist('_selected_action')
                if not selected_ids:
                    messages.error(request, 'No requests were selected.')
                    return redirect('admin:request_vehiclepartrequest_changelist')
                
                shops = form.cleaned_data['shops']
                custom_message = form.cleaned_data.get('custom_message', '')
                send_whatsapp = form.cleaned_data.get('send_whatsapp', False)
                
                # Process the assignment
                return self._process_shop_assignment(
                    request, selected_ids, shops, custom_message, send_whatsapp
                )
            else:
                # Form is invalid, show errors
                selected_ids = request.POST.getlist('_selected_action')
                selected = self.model.objects.filter(id__in=selected_ids)
        else:
            # First time showing the form - get selected items from queryset
            selected_ids = list(queryset.values_list('id', flat=True))
            selected = queryset
            form = AssignShopsForm()
        
        context = {
            **self.admin_site.each_context(request),
            'title': 'Assign Shops to Requests',
            'form': form,
            'selected': selected,
            'selected_ids': selected_ids,
            'opts': self.model._meta,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
            'media': self.media,
        }
        return render(request, 'admin/request/assign_shops_intermediate.html', context)
    
    assign_shops_action.short_description = "Assign shops to selected requests"
    
    def _process_shop_assignment(self, request, request_ids, shops, custom_message, send_whatsapp=False):
        """Process the shop assignment"""
        # Convert string IDs to integers
        request_ids = [int(id) for id in request_ids]
        requests = VehiclePartRequest.objects.filter(id__in=request_ids)
        success_count = 0
        skipped_count = 0
        whatsapp_sent = 0
        whatsapp_failed = 0
        
        for req in requests:
            # Generate message with request details
            message_parts = [
                "🚗 *Vehicle Part Request*",
                "",
                f"*Part Name:* {req.part_name}",
            ]
            
            if req.part_number:
                message_parts.append(f"*Part Number:* {req.part_number}")
            
            if req.description:
                message_parts.append(f"*Description:* {req.description}")
            
            message_parts.append(f"*Status:* {req.get_status_display()}")
            
            if custom_message:
                message_parts.append("")
                message_parts.append("*Additional Message:*")
                message_parts.append(custom_message)
            
            full_message = "\n".join(message_parts)
            
            # Create RequestHasShop entries for each shop
            for shop in shops:
                obj, created = RequestHasShop.objects.get_or_create(
                    request=req,
                    shop=shop,
                    defaults={'message': full_message}
                )
                if created:
                    success_count += 1
                else:
                    # Update message if association already exists
                    obj.message = full_message
                    obj.save()
                    skipped_count += 1
                
                # Send WhatsApp message if requested
                if send_whatsapp and shop.phone_number:
                    whatsapp_result = whatsapp_service.send_message(
                        shop.phone_number,
                        full_message
                    )
                    if whatsapp_result['success']:
                        whatsapp_sent += 1
                    else:
                        whatsapp_failed += 1
                        error_msg = whatsapp_result['message']
                        # Provide more helpful error messages
                        if 'not enabled' in error_msg.lower():
                            messages.warning(
                                request,
                                f'WhatsApp not enabled for {shop.name}. '
                                f'Please set TWILIO_WHATSAPP_ENABLED=True in your .env file and restart the server.'
                            )
                        else:
                            messages.warning(
                                request,
                                f'Failed to send WhatsApp to {shop.name}: {error_msg}'
                            )
                elif send_whatsapp and not shop.phone_number:
                    whatsapp_failed += 1
                    messages.warning(
                        request,
                        f'Cannot send WhatsApp to {shop.name}: Phone number not set. '
                        f'Please add a phone number in E.164 format (e.g., +1234567890) to the shop profile.'
                    )
        
        if success_count > 0:
            messages.success(
                request,
                f'Successfully assigned {len(shops)} shop(s) to {len(requests)} request(s). '
                f'Created {success_count} new association(s).'
            )
        if skipped_count > 0:
            messages.info(
                request,
                f'Updated {skipped_count} existing association(s) with new message.'
            )
        
        if send_whatsapp:
            if whatsapp_sent > 0:
                messages.success(
                    request,
                    f'Successfully sent {whatsapp_sent} WhatsApp message(s) to shops.'
                )
            if whatsapp_failed > 0:
                messages.error(
                    request,
                    f'Failed to send {whatsapp_failed} WhatsApp message(s). Check shop phone numbers and WhatsApp configuration.'
                )
        
        return redirect('admin:request_vehiclepartrequest_changelist')
    
