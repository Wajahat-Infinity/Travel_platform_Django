from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import logout

from core.decorators import identity_check_decorator, vendor_incomplete_decorator, branch_incomplete_decorator
from src.accounts.forms import UserProfileForm, IncompleteAgencyForm, IncompleteBranchForm
from src.accounts.models import User


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

                elif request.user.is_buyer:
                    return redirect("buyer:dashboard")

                elif request.user.is_branch:
                    return redirect("branches:dashboard")

            else:

                if request.user.is_agency:
                    return redirect('accounts:vendor-complete')

                elif request.user.is_branch:
                    return redirect('accounts:branch-complete')

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
                user.is_buyer = True
                user.is_completed = True
                user.save()
                messages.success(request, 'Your Buyer Account has Been Created Successfully')

                # notify_buyer_account_completed(user)

                return redirect('buyer:dashboard')

            elif user_type == '3':
                user.is_branch = True
                user.is_independent = True
                user.save()
                messages.success(request, 'Your Branch Account has Been Created Successfully')

                # notify_branch_account_completed(user)

                return redirect('accounts:branch-complete')

        messages.error(request, 'Some issues inside user selection make sure you are selecting the right one.')
        return redirect('accounts:identification_check')


@method_decorator(vendor_incomplete_decorator, name="dispatch")
class ProfileCompleteView(View):

    def get(self, request):
        form = IncompleteAgencyForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/complete_profile_company.html', context=context)

    def post(self, request):
        form = IncompleteAgencyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()

            user = User.objects.get(id=self.request.user.id)
            user.is_completed = True
            user.save()

            messages.success(self.request, 'Verification Has Been Completed Successfully')
            # notify_vendor_account_completed(user)
            # error, account = stripe_connect_account_create(user)

            return redirect('accounts:cross-auth')

        return render(request, template_name='accounts/complete_profile_company.html', context={'form': form})


@method_decorator(branch_incomplete_decorator, name="dispatch")
class ProfileCompleteBranchView(View):

    def get(self, request):
        form = IncompleteBranchForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/complete_profile_branch.html', context=context)

    def post(self, request):
        form = IncompleteBranchForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.branch_manager = request.user
            form.save()
            user = User.objects.get(id=self.request.user.id)
            user.is_completed = True
            user.save()

            messages.success(self.request, 'Verification Has Been Completed Successfully')
            # notify_vendor_account_completed(user)
            # error, account = stripe_connect_account_create(user)

            return redirect('accounts:cross-auth')

        return render(request, template_name='accounts/complete_profile_branch.html', context={'form': form})


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
