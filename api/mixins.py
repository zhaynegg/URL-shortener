from django.shortcuts import redirect

class SupabaseLoginRequiredMixin:

    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("supabase_access_token"):
            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)