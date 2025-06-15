from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import logout

from core.decorators import identity_check_decorator, vendor_incomplete_decorator, local_guide_incomplete_decorator, traveler_incomplete_decorator
from src.accounts.forms import UserProfileForm, IncompleteAgencyForm, IncompleteLocalGuideForm, IncompleteTravelerForm
from src.accounts.models import User
from src.web.local_guide.models import LocalGuide
from src.web.agency.models import Agency
from src.web.traveler.models import Traveler


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect("/admin/")

            if request.user.is_completed:

                if request.user.is_agency:
                    return redirect("agency:dashboard")

                elif request.user.is_local_guide:
                    return redirect("local_guide:dashboard")

                elif request.user.is_traveler:
                    return redirect("traveler:dashboard")

            else:

                if request.user.is_agency:
                    return redirect('accounts:vendor-complete')

                elif request.user.is_local_guide:
                    return redirect('accounts:local-guide-complete')
                    
                elif request.user.is_traveler:
                    return redirect('accounts:traveler-complete')

                else:
                    return redirect('accounts:identity-check')

        else:
            return redirect("account_login")


@method_decorator(identity_check_decorator, name="dispatch")
class IdentificationCheck(View):

    def get(self, request):
        return render(request, template_name='accounts/identification_check.html')

    def post(self, request):
        user_type = self.request.POST.get('user_type', None)

        if user_type:
            user = get_object_or_404(User, id=self.request.user.id)

            if user_type == '1':

                user.is_agency = True
                user.save()
                messages.success(request, 'Fill the information to Complete your Vendor Profile')
                return redirect('accounts:vendor-complete')

            elif user_type == '2':
                user.is_local_guide = True
                user.save()
                messages.success(request, 'Your Local Guide Account has Been Created Successfully')

                return redirect('accounts:local-guide-complete')

            elif user_type == '3':
                user.is_traveler = True
                user.save()
                messages.success(request, 'Your Traveler Account has Been Created Successfully')
                return redirect('accounts:traveler-complete')

        messages.error(request, 'Some issues inside user selection make sure you are selecting the right one.')
        return redirect('accounts:identification_check')


@method_decorator(vendor_incomplete_decorator, name="dispatch")
class ProfileCompleteView(View):

    def get(self, request):
        try:
            # Check if user already has an agency profile
            instance = request.user.agency_profile  # Using related_name
        except Agency.DoesNotExist:
            instance = None
            
        form = IncompleteAgencyForm(instance=instance)
        context = {'form': form}
        return render(request, 'accounts/complete_profile_company.html', context)

    def post(self, request):
        try:
            instance = request.user.agency_profile  # Get existing profile if exists
        except Agency.DoesNotExist:
            instance = None
            
        form = IncompleteAgencyForm(
            data=request.POST, 
            files=request.FILES, 
            instance=instance
        )
        
        if form.is_valid():
            agency = form.save(commit=False)  # Don't save yet
            agency.user = request.user  # Assign the user
            agency.save()  # Now save with user assigned
            form.save_m2m()  # For any many-to-many fields

            # Update user completion status
            request.user.is_completed = True
            request.user.save()

            messages.success(request, 'Profile completed successfully!')
            return redirect('accounts:cross-auth')

        return render(request, 'accounts/complete_profile_company.html', {'form': form})

@method_decorator(local_guide_incomplete_decorator, name="dispatch")
class LocalGuideCompleteView(View):

    def get(self, request):
        # Initialize form with user's existing LocalGuide data if it exists
        try:
            instance = request.user.local_guide_app_profile  # assuming related_name='localguide'
        except LocalGuide.DoesNotExist:
            instance = None
        form = IncompleteLocalGuideForm(instance=instance)
        context = {'form': form}
        return render(request, template_name='accounts/local_guide_profile_complete.html', context=context)

    def post(self, request):
        try:
            instance = request.user.local_guide_app_profile  # check if user already has a LocalGuide profile
        except LocalGuide.DoesNotExist:
            instance = None
            
        form = IncompleteLocalGuideForm(data=request.POST, files=request.FILES, instance=instance)
        
        if form.is_valid():
            local_guide = form.save(commit=False)
            local_guide.user = request.user  # Set the user before saving
            local_guide.save()
            form.save_m2m()  # Needed if you have many-to-many fields

            # Update user completion status
            user = request.user
            user.is_completed = True
            user.save()

            messages.success(request, 'Verification Has Been Completed Successfully')
            return redirect('accounts:cross-auth')

        return render(request, template_name='accounts/local_guide_profile_complete.html', context={'form': form})

@method_decorator(traveler_incomplete_decorator, name="dispatch")
class TravelerCompleteView(View):

    def get(self, request):
        try:
            # Check if user already has a traveler profile
            instance = request.user.traveler_profile  # Using related_name
        except Traveler.DoesNotExist:
            instance = None
            
        form = IncompleteTravelerForm(instance=instance)
        context = {'form': form}
        return render(request, 'accounts/traveler_profile_complete.html', context)

    def post(self, request):
        try:
            instance = request.user.traveler_profile  # Get existing profile if exists
        except Traveler.DoesNotExist:
            instance = None
            
        form = IncompleteTravelerForm(
            data=request.POST, 
            files=request.FILES, 
            instance=instance
        )
        
        if form.is_valid():
            traveler = form.save(commit=False)  # Don't save yet
            traveler.user = request.user  # Assign the user
            traveler.save()  # Now save with user assigned
            form.save_m2m()  # For any many-to-many fields

            # Update user completion status
            request.user.is_completed = True
            request.user.save()

            messages.success(request, 'Profile completed successfully!')
            return redirect('accounts:cross-auth')

        return render(request, 'accounts/traveler_profile_complete.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)
