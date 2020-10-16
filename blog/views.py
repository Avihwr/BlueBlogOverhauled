from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Blog, Contact, BlogComment, Profile, Excerpt
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from taggit.models import Tag
from django.core.mail import send_mail
from .forms import *


# Create your views here.


def footerposts(request):
    index = Blog.objects.all().order_by('-time')[0]
    context = {'index': index}
    return render(request, 'base.html', context)


def about(request):
    index1 = Blog.objects.order_by('-time').first()
    all_users = User.objects.all().distinct()
    return render(request, 'about.html', {'users': all_users, 'index1': index1})


def home(request):
    index = Blog.objects.all().order_by('-views')[0:5]
    index1 = Blog.objects.order_by('-time').first()
    # time = time_to_read(index1.content)
    # print(time)
    context = {'index': index, 'index1': index1}
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def posts_list(request):
    blogs = Blog.objects.all().order_by('-time')
    post_list = Blog.objects.filter(user=request.user)
    context = {'posts': post_list, 'Blogs': blogs}
    return render(request, 'post_list.html', context)


def blog(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    blogs = Blog.objects.all().order_by('-time')
    blog1 = Blog.objects.all().order_by('-time')[0:4]
    blog2 = Blog.objects.all().order_by('-time')[4:]
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    number = paginator.page_range
    pagy = paginator.get_page(page_number)
    context = {'number': number, 'Blogs': blogs, 'page': pagy, 'blog': blog1, 'blog1': blog2,
               'index1': index1}
    return render(request, 'bloghome.html', context)


@permission_required('blog.add_blog', raise_exception=True)
@login_required(login_url="/login/")
def post_upload(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    content = request.POST.get('content')
    title = request.POST.get('title')
    image = request.FILES.get('image')
    time = time_to_read(str(content))
    if request.method == 'POST':
        post_form = PostUpload(request.POST, request.FILES, instance=request.user)
        if post_form.is_valid():
            tags = post_form.cleaned_data['tags']
            context = post_form.cleaned_data['context']
            excerpt_type = post_form.cleaned_data['excerpt_type']
            ins = Blog.objects.create(time_to_read=time, user=request.user, content=content, title=title, image=image,
                                      context=context,
                                      excerpt_type=excerpt_type)
            ins.save()
            for tag in tags:
                ins.tags.add(tag)
            messages.success(request, 'Your Post has been successfully posted')
            print(request.POST)
            print(tags)
            return redirect('posts', slug=ins.slug)
        else:
            print(f'error in {request.POST}')
    else:
        post_form = PostUpload(instance=request.user)
    context = {'post_form': post_form, 'index1': index1}
    return render(request, 'post_upload.html', context)


@login_required(login_url="/login/")
def excerpt(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    if request.method == 'POST':
        tag_form = ExcerptForm(request.POST or None)
        if tag_form.is_valid():
            tag_form.save()
            messages.success(request, 'Your Excerpt has been submitted successfully')
            return HttpResponseRedirect(reverse('excerpt'))
    else:
        tag_form = ExcerptForm()
    context = {'tag_form': tag_form, 'index1': index1}
    return render(request, 'excerpt.html', context)


@permission_required('blog.delete_blog', raise_exception=True)
@login_required(login_url="/login/")
def post_delete(request, slug):
    post = Blog.objects.filter(slug=slug).first()
    post.delete()
    messages.success(request, "Your post has been deleted successfully")
    return HttpResponseRedirect(reverse('post_list'))


@login_required(login_url="/login/")
def comment_delete(request, sno):
    comment = get_object_or_404(BlogComment, sno=sno)
    comment.delete()
    return redirect('posts', slug=comment.post.slug)


@login_required(login_url="/login/")
def reply_delete(request, sno, parent_id):
    comment = get_object_or_404(BlogComment, sno=sno)
    x = comment.replies.filter(parent_id=parent_id).order_by('-replies__time').first()
    x.delete()
    return redirect('posts', slug=comment.post.slug)


@permission_required('blog.change_blog', raise_exception=True)
@login_required(login_url="/login/")
def post_edit(request, pk):
    index1 = Blog.objects.all().order_by('-time')[0]
    post = get_object_or_404(Blog, pk=pk)
    user = request.user
    if request.method == 'POST':
        edit_form = PostEdit(request.POST or None, request.FILES, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            print(request.POST)
            messages.success(request, 'Your Post has been updated successfully')
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        edit_form = PostEdit(instance=post)
    context = {'edit_form': edit_form, 'post': post, 'user': user, 'index1': index1}
    return render(request, 'post_edit.html', context)


# def pagination(request):
#     post = Blog.objects.all()
#     paginator = Paginator(post, 1)
#     page_number = request.GET.get['page']
#     blogs = paginator.get_page(page_number)
#     context = {'blogs': blogs}
#     return render(request, 'bloghome.html', context)


def posts(request, slug):
    try:
        index1 = Blog.objects.all().order_by('-time')[0]
        index2 = Blog.objects.all().order_by('-time')[0:5]
        index3 = list(set(Blog.objects.all().order_by('-tags')))[0:6]
        index4 = list(set(BlogComment.objects.all().order_by('-time')))[0:6]
        lst = Blog.objects.all().order_by('-time')
        tag = []
        tagi = []
        for dist in lst:
            if dist.context not in tag:
                print(dist)
                tag.append(dist.context)
            if dist.excerpt_type.excerpt not in tagi:
                tagi.append(dist.excerpt_type.excerpt)
        tags = zip(tag, tagi)
        common_tags = Blog.tags.most_common()[:4]
        post = Blog.objects.filter(slug=slug).first()
        post.views = post.views + 1
        post.save()
        comments = BlogComment.objects.filter(post=post, parent=None)
        user = request.user

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = request.POST.get('comment')
                parentSno = request.POST.get('parentSno')
                if parentSno == " ":
                    ins = BlogComment.objects.create(post=post, user=user, comment=comment)
                    ins.save()
                    send_mail(
                        'Someone commented on your post -> ' + ins.post.title,
                        ins.user.username + ' said ' + comment,
                        ins.user.email,
                        ['avihwr@gmail.com', ins.post.user.email],
                        fail_silently=False,
                    )
                else:
                    parent = BlogComment.objects.get(sno=parentSno)
                    ins = BlogComment.objects.create(post=post, user=user, comment=comment, parent=parent)

                ins.save()
                messages.success(request, 'Your comment has been successfully posted')
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()
        context = {'tag': common_tags, 'tags': tags, 'Blog': post, 'comments': comments, 'user': user,
                   'form': comment_form,
                   'index1': index1,
                   'index2': index2,
                   'index3': index3,
                   'index4': index4[0:4]}
        return render(request, 'blogposts.html', context)
    except AttributeError:
        return HttpResponse('<h1 style="font-family:Poppins, sans-serif;">Wrong slug matched<h1>'
                            '<h2 style="font-family:Poppins, sans-serif;">Post does not exist<h2>')


def contact(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        desc = request.POST.get('desc')

        if len(name) < 2:
            messages.warning(request, "Please enter a valid name")
        elif len(email) < 3:
            messages.warning(request, 'Please enter a valid email address')
        elif len(desc) < 4:
            messages.warning(request, 'Please elaborate your concern')
        else:
            ins = Contact(name=name, email=email, desc=desc, subject=subject)
            ins.save()
            send_mail(
                subject + ' by ' + name,
                desc,
                email,
                ['avihwr@gmail.com'],
                fail_silently=False,
            )
            print('done')
    context = {'index1': index1}
    return render(request, 'contact.html', context)


@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def login(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    if request.method == 'POST':
        loginname = request.POST.get('username')
        loginpass = request.POST.get('password')

        user = authenticate(username=loginname, password=loginpass)

        if user is not None:
            auth_login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Your username and password didn't match. Please try again.")
    context = {'index1': index1}
    return render(request, "registration/login.html", context)


def tagged(request, slug):
    index1 = Blog.objects.all().order_by('-time')[0]
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    blogs = Blog.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'page': blogs,
        'index1': index1
    }
    return render(request, 'bloghome.html', context)


def Category(request, category):
    index1 = Blog.objects.all().order_by('-time').first()
    category = Blog.objects.filter(context__icontains=category).order_by('-time')
    print(category)
    # Filter posts by tag name
    # blogs = Blog.objects.filter(context=category.all()).first()
    context = {
        'tag': category,
        'page': category,
        'index1': index1
    }
    return render(request, 'bloghome.html', context)


@login_required(login_url="/login/")
def profile_edit(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    if request.method == 'POST':
        user_form = UserEditForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'user_form': user_form, "profile_form": profile_form, 'index1': index1}
    return render(request, 'profile.html', context)


def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("/")


def search(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    query = request.GET['query']
    if len(query) > 80:
        queryposts = Blog.objects.none()
    else:
        querypostsTitle = Blog.objects.filter(Q(title__icontains=query))
        querypostsContent = Blog.objects.filter(Q(content__icontains=query))
        # querypostsTC = querypostsTitle.union(querypostsContent) #Cannot use nested unions with Mysql DB
        querypostsAuthor = Blog.objects.filter(Q(user__username__icontains=query))
        querypostsExcerpt = Blog.objects.filter(Q(excerpt_type__excerpt__icontains=query))
        querypostsContext = Blog.objects.filter(Q(context__icontains=query))
        # queryposts1 = querypostsAuthor.union(querypostsTC) #Cannot use nested unions with Mysql DB
        queryposts = querypostsTitle | querypostsExcerpt | querypostsContent | querypostsAuthor | querypostsContext

    if queryposts.count() == 0:
        messages.warning(request, "No Search Results Found. Please Refine Your Query")
    context = {'QueryPosts': queryposts, 'query': query, 'index1': index1}
    return render(request, 'search.html', context)


# random redirects


def posts_redirect(request):
    return HttpResponseRedirect(reverse('blog'))


def posts_edit_redirect(request):
    return HttpResponseRedirect(reverse('post_list'))


# misc function to calculate data
# function to get unique values only out of lists


# def unique_values(list1):
#     # intilize a null list
#     unique_list = []
#
#     # traverse for all elements
#     for x in list1:
#         # check if exists in unique_list or not
#         if x not in unique_list:
#             unique_list.append(x)
#             # print list
#             return unique_list


def time_to_read(content):
    x = len(content) / 700
    return round(x)
