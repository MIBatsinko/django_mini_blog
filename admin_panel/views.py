from django.shortcuts import render


class BlogHomePage:
    def home(self):
        return render(self, 'admin_panel/dashboard.html')
