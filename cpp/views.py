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
        d = int(request.POST['min_degree']) if request.POST['min_degree'] else 0
        w = int(request.POST['max_weight']) if request.POST['max_weight'] else None
        s = int(request.POST['start_node']) if request.POST['start_node'] else None
        context['ret'], context['nodes'], context['oriedges'], context['path'] \
            = solver(degree=d, weight=w, start=s)
        FileSystemStorage().delete('graph.csv')
    return render(request, 'cpp.html', context)