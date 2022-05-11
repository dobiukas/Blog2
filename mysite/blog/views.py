from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Post
from .forms import CommentForm, CreateUserForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
class PostDetailView(generic.DetailView, FormMixin):
    model = Post
    template_name = 'project.html'
    context_object_name = 'project'
    form_class = CommentForm

    class Meta:
        ordering = ['title']

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.Comment = self.request.user
        form.save()
        return super(PostDetailView, self).form_valid(form)


###comments


# signup page
def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('/blog')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('/blog/login')

        context = {'form': form}
        return render(request, 'register.html', context)

# login page
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('/blog')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'login.html', context)


# logout page
def LogOutPage(request):
    logout(request)
    return redirect('/blog')
#comments

def post_detail(request, slug):
    template_name = 'post_detail.html'
    paginate_by = 3
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():


            new_comment = comment_form.save(commit=False)

            new_comment.post = post

            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})





