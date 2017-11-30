from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from cppsolver import solver

# Create your views here.
def cpp(request):
    context = {}
    if 'uploadgraph' in request.FILES:
        uploadgraph = request.FILES['uploadgraph']
        fs = FileSystemStorage()
        filename = fs.save('graph.csv', uploadgraph)
        context['ret']=solver()
        FileSystemStorage().delete('graph.csv')
    return render(request, 'cpp.html', context)