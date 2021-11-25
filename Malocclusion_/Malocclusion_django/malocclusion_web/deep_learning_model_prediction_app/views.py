from django.shortcuts import render

# Create your views here.
from .models import model_prediction_class
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect


class PhotoUploadView(CreateView):
    model = model_prediction_class
    fields = ['photo']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class PhotoDeleteView(DeleteView):
    model = model_prediction_class
    success_url = '/'
    template_name = 'photo/delete.html'


class PhotoUpdateView(UpdateView):
    model = model_prediction_class
    fields = ['deep_learning_model_prediction_app']
    template_name = 'photo/update.html'


def photo_list(request):
    photos = model_prediction_class.objects.all()
    return render(request, 'photo/list.html', {'photos': photos})
