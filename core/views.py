from django.shortcuts import render, redirect
from core.models import *
from userauths.models import Profile, User
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Random
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
@login_required
def newsfeed(request):
    profile_user = Profile.objects.get(user = request.user)
    user_friends = Friend.objects.filter(user=request.user)
    user_liked_pages = LikedPage.objects.filter(user=request.user)
    profiles = [friend.friend_profile for friend in user_friends]
    profiles += [liked_page.profile for liked_page in user_liked_pages]
    

    all_pages = None
    if Page.objects.all():
        all_pages = Page.objects.all().order_by(Random())
    all_people = Profile.objects.exclude(user=request.user).order_by(Random())
    post = Posts.objects.filter(
        Q(profile__in=profiles) | Q(page__in=user_liked_pages.values('page')) |Q(user=request.user)
        ).order_by("-id")
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    user = request.user
    profile_for_post_creation = Profile.objects.get(user = user)
    stories = Story.objects.all().order_by("-id")

    if request.method == "POST":
        if "add_post" in request.POST:
            content = request.POST.get("content")
            image = request.FILES.get("image")
            video = request.FILES.get("video")
            new_post = Posts.objects.create(
                user=request.user,
                profile=profile_for_post_creation,
                content=content,
                image=image,
                video=video,
            )
            if Friend.objects.filter(user=request.user).exists():
                friends = Friend.objects.filter(user=request.user)
                for f in friends:
                    Notification.objects.create(
                        sent_to = f.friend_user,
                        sent_to_profile = f.friend_profile,
                        profile = profile_user,
                        post = new_post,
                        body = "added a post",
                    )
                Notification.objects.create(
                    sent_to = request.user,
                    sent_to_profile = profile_user,
                    post = new_post,
                    body = "Your post was uploaded",
                )
            

            return redirect("/") 
        elif "delete_post" in request.POST:
            post_id = request.POST.get("id")
            delete_post = Posts.objects.get(id=post_id)
            if SharedPost.objects.filter(original_post_id = post_id).exists():
                delete_shared_post = SharedPost.objects.filter(original_post_id = post_id)
                delete_shared_post.delete()
            delete_post.delete()
            Notification.objects.create(
                sent_to = request.user,
                sent_to_profile = profile_user,
                body = "Your post was deleted"
            )
            return redirect("/")
        elif "add-comment" in request.POST:
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment')
            image_file = request.FILES.get('image')
            post = Posts.objects.get(id=post_id)
            profile_c = Profile.objects.get(user=request.user)
            new_comment = Comment.objects.create(
                user = request.user,
                post = post,
                comment = comment_text,
                profile = profile_c,
            )
            if image_file:
                new_comment.image = image_file
            new_comment.save()
            post.comments += 1
            post.save()
            if post.page:
                Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                page = post.page,
                profile = profile_user,
                body = f"commented on your page {post.page.name}'s post",
                post = post
            )
            elif post.user == request.user:
                pass
            elif post.shared_post:
                Notification.objects.create(
                    sent_to=post.user,
                    sent_to_profile=post.profile,
                    profile = profile_user,
                    body = "commented on a post you shared",
                    post = post
                )
            else:
                Notification.objects.create(
                    sent_to=post.user,
                    sent_to_profile=post.profile,
                    profile = profile_user,
                    body = "commented on your post",
                    post = post
                )
            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"

            return redirect(redirect_url)
        elif "delete_comment" in request.POST:
            post_id = request.POST.get("id")
            cid = request.POST.get("cid")
            that_post = Posts.objects.get(id=post_id)
            delete_comment = Comment.objects.get(cid=cid)
            delete_comment.delete()
            that_post.comments -= 1
            that_post.save()

            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"
            return redirect(redirect_url)
        elif 'unique_file_input_name' in request.FILES:
            file = request.FILES['unique_file_input_name']

            # Check the file type
            if file.content_type.startswith('image'):
                # File is an image, save it to the image attribute
                Story.objects.create(user=request.user, profile=profile_user, image=file)
            elif file.content_type.startswith('video'):
                # File is a video, save it to the video attribute
                Story.objects.create(user=request.user, profile=profile_user, video=file)
            return redirect("/")
        elif "delete_story" in request.POST:
            id = request.POST.get("id")
            delete_story = Story.objects.get(id=id)
            delete_story.delete()
            return redirect("/")

    context = {
        "all_people": all_people,
        "profile_user": profile_user,
        "post": post,
        "liked_post_ids":liked_post_ids,
        "stories":stories,
        "all_pages":all_pages,
    }
    return render(request, "core/newsfeed.html", context)

@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    pages = None
    if Page.objects.filter(user=user).exists():
        pages = Page.objects.filter(user=user)
    friend_request = None
    if FriendRequest.objects.filter(reciever_user = request.user, sender_user = user, is_friend = False).exists():
        friend_request = FriendRequest.objects.get(reciever_user = request.user, sender_user = user, is_friend = False)
    sent_request = None
    if FriendRequest.objects.filter(sender_user = request.user, reciever_user = user, is_friend = False).exists():
        sent_request = FriendRequest.objects.get(sender_user = request.user, reciever_user = user, is_friend = False) 
    is_friend = None
    profile_user = Profile.objects.get(user = request.user)
    if Friend.objects.filter(friend_profile = profile, profile = profile_user).exists():
        is_friend = Friend.objects.get(friend_profile = profile, profile = profile_user)
    post = Posts.objects.filter(user=user, profile=profile).order_by("-id")
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    info = None
    if General_information.objects.filter(user=request.user).exists():
        info = General_information.objects.get(user=user)
    current_user = request.user
    profile_for_post_creation = Profile.objects.get(user = current_user)
    friend_list = None
    if Friend.objects.filter(profile = profile).exists():
        friend_list = Friend.objects.filter(profile = profile)

    if request.method == "POST":
        if "add_post" in request.POST:
            content = request.POST.get("content")
            image = request.FILES.get("image")
            video = request.FILES.get("video")
            new_post = Posts.objects.create(
                user=request.user,
                profile = profile_for_post_creation,
                content=content,
                image=image,
                video=video,
            )
            if Friend.objects.filter(user=request.user).exists():
                friends = Friend.objects.filter(user=request.user)
                for f in friends:
                    Notification.objects.create(
                        sent_to = f.friend_user,
                        sent_to_profile = f.friend_profile,
                        profile = profile_user,
                        post = new_post,
                        body = "added a post",
                    )
                Notification.objects.create(
                    sent_to = request.user,
                    sent_to_profile = profile_user,
                    post = new_post,
                    body = "Your post was uploaded",
                )
            id = request.user.id
            profile_url = reverse('core:profile', args=[id])

            return redirect(profile_url) 
        elif "delete_post" in request.POST:
            post_id = request.POST.get("id")
            delete_post = Posts.objects.get(id=post_id)
            if SharedPost.objects.filter(original_post_id = post_id).exists():
                delete_shared_post = SharedPost.objects.filter(original_post_id = post_id)
                delete_shared_post.delete()
            delete_post.delete()
            Notification.objects.create(
                sent_to = request.user,
                sent_to_profile = profile_user,
                body = "Your post was deleted"
            )
            id = request.user.id
            profile_url = reverse('core:profile', args=[id])

            return redirect(profile_url)
        elif "add-comment" in request.POST:
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment')
            image_file = request.FILES.get('image')
            post = Posts.objects.get(id=post_id)
            profile_c = Profile.objects.get(user=request.user)
            new_comment = Comment.objects.create(
                user = request.user,
                post = post,
                comment = comment_text,
                profile = profile_c,
            )
            if image_file:
                new_comment.image = image_file
            new_comment.save()
            post.comments += 1
            post.save()
            if post.page:
                Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                page = post.page,
                profile = profile_user,
                body = f"commented on your page {post.page.name}'s post",
                post = post
            )
            elif post.user == request.user:
                pass
            elif post.shared_post:
                Notification.objects.create(
                    sent_to=post.user,
                    sent_to_profile=post.profile,
                    profile = profile_user,
                    body = "commented on a post you shared",
                    post = post
                )
            else:
                Notification.objects.create(
                    sent_to=post.user,
                    sent_to_profile=post.profile,
                    profile = profile_user,
                    body = "commented on your post",
                    post = post
                )
            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"

            return redirect(redirect_url)
        elif "delete_comment" in request.POST:
            post_id = request.POST.get("id")
            cid = request.POST.get("cid")
            that_post = Posts.objects.get(id=post_id)
            delete_comment = Comment.objects.get(cid=cid)
            delete_comment.delete()
            that_post.comments -= 1
            that_post.save()

            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"
            return redirect(redirect_url)
        elif "delete_request" in request.POST:
            profile_id = request.POST.get("profile_id")
            user_id = request.POST.get("user_id")
            delete_request = FriendRequest.objects.get(sender_profile__id = profile_id)
            delete_request.delete()

            return redirect("core:profile", user_id)
        elif "add_friend" in request.POST:
            profile_id = request.POST.get('profile_id')
            reciever_profile = Profile.objects.get(id=profile_id)
            FriendRequest.objects.create(
                sender_profile = profile_for_post_creation,
                reciever_profile = reciever_profile,
                sender_user = request.user,
                reciever_user = reciever_profile.user
            )
            return redirect("core:profile", reciever_profile.user.id)
        elif "cancel_sent_request" in request.POST:
            profile_id = request.POST.get('profile_id')
            reciever_profile = Profile.objects.get(id=profile_id)
            profile_user_id = Profile.objects.get(id=profile_id)
            delete_friend_request = FriendRequest.objects.get(reciever_profile=reciever_profile)
            delete_friend_request.delete()
            return redirect("core:profile", profile_user_id.user.id)
        elif "accept_request" in request.POST:
            profile_id = request.POST.get('profile_id')
            user_id = request.POST.get('user_id')
            friend_profile = Profile.objects.get(id = profile.id)
            user_profile = Profile.objects.get(user=request.user)
            Friend.objects.create(
                profile=user_profile,
                user = request.user,
                friend_profile=friend_profile,
                friend_user=friend_profile.user
            )
            Friend.objects.create(
                profile = friend_profile,
                user = friend_profile.user,
                friend_profile = user_profile,
                friend_user = user_profile.user
            )
            Notification.objects.create(
                sent_to = friend_profile.user,
                sent_to_profile = friend_profile,
                profile = profile_user,
                body = "accepted your friend request",
                friends = True,
            )
            sender_profile = Profile.objects.get(id=profile_id)
            delete_friend_request = FriendRequest.objects.get(sender_profile=sender_profile, reciever_user = request.user)
            delete_friend_request.delete()
            return redirect("core:profile", user_id)
        elif "unfriend_user" in request.POST:
            id = request.POST.get("id")
            profile = Profile.objects.get(id=id)
            user_profile = Profile.objects.get(user=request.user)
            delete_friend1 = Friend.objects.get(profile = profile, friend_profile = user_profile)
            delete_friend2 = Friend.objects.get(profile = user_profile, friend_profile=profile)
            delete_friend1.delete()
            delete_friend2.delete()
            return redirect("core:profile", profile.user.id)

        
    context = {
        "profile": profile,
        "profile_user": profile_user,
        "user": user,
        "post": post,
        "info":info,
        "liked_post_ids":liked_post_ids,
        "friend_request": friend_request,
        "sent_request": sent_request,
        "is_friend": is_friend,
        "friend_list": friend_list,
        "pages": pages,
        
    }
    return render(request, "core/profile.html", context)

@login_required
def create_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        return redirect("core:profile", request.user.id)
    elif request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        bio = request.POST.get("bio")
        phone_no = request.POST.get("phone_no")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthday")
        city = request.POST.get("city")
        country = request.POST.get("country")
        profile_pic = request.FILES.get("profile_pic")
        cover_pic = request.FILES.get("cover_pic")

        new_profile = Profile.objects.create(
            user = request.user,
            firstname = firstname,
            lastname = lastname,
            bio = bio,
            phone_no = phone_no,
            gender = gender,
            birthday = birthday,
            city = city,
            country = country,
            profile_pic = profile_pic,
            cover_pic = cover_pic
        )
        new_profile.save()
        General_information.objects.create(user=request.user)
        Notification.objects.create(
            sent_to = request.user,
            sent_to_profile = new_profile,
            body = f"Welcome to Facebook" 
        )
        id = request.user.id
        profile_url = reverse('core:profile', args=[id])

        return redirect(profile_url)

    return render(request, "core/create-profile.html")

@login_required
def edit_account(request):
    profile = Profile.objects.get(user=request.user)
    info = General_information.objects.get(user = request.user)
    if request.method == "POST":
        form_name = request.POST.get("name")
        if "profile_submit" in request.POST:
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            username = request.POST.get("username")
            email = request.POST.get("email")
            bio = request.POST.get("bio")
            phone_no = request.POST.get("phone_no")
            gender = request.POST.get("gender")
            birthday = request.POST.get("birthday")
            city = request.POST.get("city")
            country = request.POST.get("country")
            profile_pic = request.FILES.get("profile_pic")
            cover_pic = request.FILES.get("cover_pic")

            update_user = User.objects.get(id=request.user.id) 
            update_user.username = username
            update_user.email = email
            update_user.save()

            update_profile = Profile.objects.get(user=request.user)
            update_profile.firstname = firstname
            update_profile.lastname = lastname
            update_profile.bio = bio
            update_profile.phone_no = phone_no
            update_profile.gender = gender
            update_profile.birthday = birthday
            update_profile.city = city
            update_profile.country = country
            
            # Check if profile_pic or cover_pic has changed
            if profile_pic is not None and profile_pic != update_profile.profile_pic:
                update_profile.profile_pic = profile_pic
                
                # Create a post for profile image change
                post = Posts.objects.create(user=request.user, profile=profile, content="Updated profile image", image=profile_pic)
                post.save()
                Notification.objects.create(
                    sent_to = request.user,
                    sent_to_profile = profile,
                    body = f"Your Profile picture was updated"
                )
                if Friend.objects.filter(user=request.user).exists():
                    friends = Friend.objects.filter(user=request.user)
                    for f in friends:
                        Notification.objects.create(
                            sent_to = f.friend_user,
                            sent_to_profile = f.friend_profile,
                            profile = profile,
                            post = post,
                            body = "updated their <span style=\"color: #1877f2;\">profile picture</span>",
                        )
            else:
                update_profile.profile_pic = update_profile.profile_pic
                
            if cover_pic is not None and cover_pic != update_profile.cover_pic:
                update_profile.cover_pic = cover_pic
                
                # Create a post for cover image change
                post = Posts.objects.create(user=request.user, profile=profile, content="Updated cover image", image=cover_pic)
                post.save()
                Notification.objects.create(
                    sent_to = request.user,
                    sent_to_profile = profile,
                    body = f"Your Cover picture was updated"
                )
                if Friend.objects.filter(user=request.user).exists():
                    friends = Friend.objects.filter(user=request.user)
                    for f in friends:
                        Notification.objects.create(
                            sent_to = f.friend_user,
                            sent_to_profile = f.friend_profile,
                            profile = profile,
                            post = post,
                            body = "updated their <span style=\"color: #1877f2;\">cover picture</span>",
                        )
            else:
                update_profile.cover_pic = update_profile.cover_pic

            update_profile.save()
            Notification.objects.create(
                sent_to = request.user,
                sent_to_profile = profile,
                body = f"Your Profile was updated.."
            )

            id = request.user.id
            profile_url = reverse('core:profile', args=[id])

            return redirect(profile_url)
        
        elif "info_submit" in request.POST:
            education = request.POST.get("education")
            work_experience = request.POST.get("work_experience")
            other_interests = request.POST.get("other_interests")
            hobbies = request.POST.get("hobbies")

            updated_info = General_information.objects.get(user = request.user)
            updated_info.education = education
            updated_info.work_experience = work_experience
            updated_info.other_interests = other_interests
            updated_info.hobbies = hobbies
            updated_info.save()
            Notification.objects.create(
                sent_to = request.user,
                sent_to_profile = profile,
                body = f"Your Profile was updated.."
            )
            id = request.user.id
            profile_url = reverse('core:profile', args=[id])

            return redirect(profile_url)
        
    context = {
        "profile":profile,
        "info":info,
    }
    return render(request, "core/settings.html", context)

@csrf_exempt
def like(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        
        post = Posts.objects.get(id=post_id)
        if Like.objects.filter(post=post , user = request.user).exists():
                # User already liked the post, so unlike it
            delete_like = Like.objects.get(post=post, user=request.user)
            delete_like.delete()
            post.likes -= 1
        else:
                # User didn't like the post, so like it
            new_like = Like.objects.create(user = request.user, post=post)
            post.likes += 1
            if post.page:
                Notification.objects.create(
                    sent_to = post.user,
                    sent_to_profile = post.profile,
                    profile = profile,
                    post=post,
                    body = f"liked your page <span style=\"color: #1877f2;\">{post.page.name}</span>'s post",
            )
            else:
                Notification.objects.create(
                    sent_to = post.user,
                    sent_to_profile = post.profile,
                    profile = profile,
                    post=post,
                    body = f"liked your post",
            )
        post.save()
            
            # Return the updated likes count as JSON response
        return JsonResponse({'likes': post.likes})

@login_required
def post_details(request, id):
    post = Posts.objects.get(id=id)
    profile = Profile.objects.get(user=post.user)
    profile_user = Profile.objects.get(user = request.user)
    try:
        liked = Like.objects.get(post = post, user = request.user)
    except:
        liked = None
    if "add-comment" in request.POST:
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment')
        image_file = request.FILES.get('image')
        post = Posts.objects.get(id=post_id)
        profile_c = Profile.objects.get(user=request.user)
        new_comment = Comment.objects.create(
            user = request.user,
            post = post,
            comment = comment_text,
            profile = profile_c,
        )
        if image_file:
            new_comment.image = image_file
        new_comment.save()
        post.comments += 1
        post.save()
        if post.page:
            Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                page = post.page,
                profile = profile_user,
                body = f"commented on your page {post.page.name}'s post",
                post = post
            )
        elif post.page:
            Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                page = post.page,
                profile = profile_user,
                body = f"commented on your page {post.page.name}'s post",
                post = post
            )
        elif post.user == request.user:
            pass

        elif post.shared_post:
            Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                profile = profile_user,
                body = "commented on a post you shared",
                post = post
            )
        else:
            Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                profile = profile_user,
                body = "commented on your post",
                post = post
            )
        redirect_url = redirect("core:post", post_id).url
        redirect_url += "#comments"
        return redirect(redirect_url)
    elif "delete_comment" in request.POST:
        post_id = request.POST.get("id")
        cid = request.POST.get("cid")
        that_post = Posts.objects.get(id=post_id)
        delete_comment = Comment.objects.get(cid=cid)
        delete_comment.delete()
        that_post.comments -= 1
        that_post.save()

        redirect_url = redirect("core:post", post_id).url
        redirect_url += "#comments"
        return redirect(redirect_url)
    elif "delete_post" in request.POST:
        post_id = request.POST.get("id")
        delete_post = Posts.objects.get(id=post_id)
        if SharedPost.objects.filter(original_post_id = post_id).exists():
            delete_shared_post = SharedPost.objects.filter(original_post_id = post_id)
            delete_shared_post.delete()
        delete_post.delete()
        Notification.objects.create(
                sent_to = request.user,
                sent_to_profile = profile_user,
                body = "Your post was deleted"
            )
        id = request.user.id
        profile_url = reverse('core:profile', args=[id])

        return redirect(profile_url)
            
    context = {
        "profile":profile,
        "profile_user": profile_user,
        "p": post,
        "liked": liked,
    }
    return render(request, "core/post-details.html", context)

@csrf_exempt
def share_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('original_post_id')
        new_post_content = request.POST.get('new_post_content')
        post = Posts.objects.get(id=post_id)
        new_shared_post = SharedPost.objects.create(
            user = post.user,
            profile = post.profile,
            image = post.image,
            video = post.video,
            page = post.page,
            content = post.content,
            original_post_id = post_id,
        )
        new_shared_post.save()
        post.shares +=1
        post.save()
        post_profile = Profile.objects.get(user = request.user)
        new_post = Posts.objects.create(
            user=request.user,
            profile = post_profile,
            content = new_post_content,
            shared_post = new_shared_post
        )
        new_post.save()
        if Friend.objects.filter(user=request.user).exists():
            friends = Friend.objects.filter(user=request.user)
            if new_post.shared_post.page:
                for f in friends:
                    Notification.objects.create(
                        sent_to = f.friend_user,
                        sent_to_profile = f.friend_profile,
                        profile = new_post.profile,
                        post = new_post,
                        body = f"shared <span style=\"color: #1877f2;\">{new_post.shared_post.page.name}</span>'s post"
                    )
            else:
                for f in friends:
                    Notification.objects.create(
                        sent_to = f.friend_user,
                        sent_to_profile = f.friend_profile,
                        profile = new_post.profile,
                        post = new_post,
                        body = f"shared <span style=\"color: #1877f2;\">{new_post.shared_post.profile.firstname} {new_post.shared_post.profile.lastname}</span>'s post"
                    )
        return JsonResponse({'success':True})

@login_required
def videos(request):
    profile_user = Profile.objects.get(user = request.user)
    post = Posts.objects.all().order_by(Random())
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    if request.method == "POST":
        
        if "delete_post" in request.POST:
            post_id = request.POST.get("id")
            delete_post = Posts.objects.get(id=post_id)
            if SharedPost.objects.filter(original_post_id = post_id).exists():
                delete_shared_post = SharedPost.objects.filter(original_post_id = post_id)
                delete_shared_post.delete()
            delete_post.delete()
            Notification.objects.create(
                sent_to = request.user,
                sent_to_profile = profile_user,
                body = "Your Video was deleted"
            )
            return redirect("core:videos")
        elif "add-comment" in request.POST:
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment')
            image_file = request.FILES.get('image')
            post = Posts.objects.get(id=post_id)
            profile_c = Profile.objects.get(user=request.user)
            new_comment = Comment.objects.create(
                user = request.user,
                post = post,
                comment = comment_text,
                profile = profile_c,
            )
            if image_file:
                new_comment.image = image_file
            new_comment.save()
            post.comments += 1
            post.save()
            if post.page:
                Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                page = post.page,
                profile = profile_user,
                body = f"commented on your page {post.page.name}'s post",
                post = post
            )
            elif post.user == request.user:
                pass
            else:
                Notification.objects.create(
                    sent_to=post.user,
                    sent_to_profile=post.profile,
                    profile = profile_user,
                    body = "commented on your post",
                    post = post
                )
            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"

            return redirect(redirect_url)
        elif "delete_comment" in request.POST:
            post_id = request.POST.get("id")
            cid = request.POST.get("cid")
            that_post = Posts.objects.get(id=post_id)
            delete_comment = Comment.objects.get(cid=cid)
            delete_comment.delete()
            that_post.comments -= 1
            that_post.save()

            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"
            return redirect(redirect_url)
    context = {
        "profile_user": profile_user,
        "post": post,
        "liked_post_ids":liked_post_ids,
    }
    return render(request, "core/videos.html", context)

@login_required
def friend_requests(request):
    friend_request = FriendRequest.objects.filter(reciever_user = request.user)
    context = {
        "friend_request": friend_request,
    }
    return render(request, "core/friend-requests.html", context)

@csrf_exempt
def delete_friend_request(request):
    if request.method == 'POST':
        fri_req_id = request.POST.get('fri_req_id')
        delete_request = FriendRequest.objects.get(fri_req_id=fri_req_id)
        delete_request.delete()

        return JsonResponse({'success':True})
    
@csrf_exempt
def accept_friend_request(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        sender_profile_id = request.POST.get('sender_profile_id')
        sender_profile = Profile.objects.get(id=sender_profile_id)
        Friend.objects.create(
            profile=profile,
            user = profile.user,
            friend_profile = sender_profile,
            friend_user = sender_profile.user,
        )
        Friend.objects.create(
            profile=sender_profile,
            user = sender_profile.user,
            friend_profile = profile,
            friend_user = profile.user
        )
        Notification.objects.create(
            sent_to = sender_profile.user,
            sent_to_profile = sender_profile,
            profile = profile,
            body = "accepted your friend request",
            friends = True,
        )
        delete_friend_request= FriendRequest.objects.get(sender_profile=sender_profile, reciever_user=request.user)
        delete_friend_request.delete()
        return JsonResponse({'success':True})

@login_required  
def page(request, id):
    page = Page.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    post = Posts.objects.filter(page=page).order_by("-id")
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    liked = None
    if LikedPage.objects.filter(user=request.user).exists():
        liked = LikedPage.objects.get(user=request.user)
    liked_by = None
    if LikedPage.objects.filter(page=page).exists():
        liked_by = LikedPage.objects.filter(page=page)
        
    if request.method == "POST":
        if "add_post" in request.POST:
            content = request.POST.get("content")
            image = request.FILES.get("image")
            video = request.FILES.get("video")
            new_post = Posts.objects.create(
                user=request.user,
                page=page,
                content=content,
                image=image,
                video=video,
            )
            if LikedPage.objects.filter(page=new_post.page).exists():
                liked_by = LikedPage.objects.filter(page=new_post.page)
                for l in liked_by:
                    Notification.objects.create(
                        sent_to = l.profile.user,
                        sent_to_profile = l.profile,
                        page = new_post.page,
                        body = "added a post",
                    )
            id = page.id
            page_url = reverse('core:page', args=[id])

            return redirect(page_url) 
        elif "delete_post" in request.POST:
            post_id = request.POST.get("id")
            delete_post = Posts.objects.get(id=post_id)
            if SharedPost.objects.filter(original_post_id = post_id).exists():
                delete_shared_post = SharedPost.objects.filter(original_post_id = post_id)
                delete_shared_post.delete()
            delete_post.delete()
            id = page.id
            page_url = reverse('core:page', args=[id])

            return redirect(page_url)
        elif "add-comment" in request.POST:
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment')
            image_file = request.FILES.get('image')
            post = Posts.objects.get(id=post_id)
            profile_c = Profile.objects.get(user=request.user)
            new_comment = Comment.objects.create(
                user = request.user,
                post = post,
                comment = comment_text,
                profile = profile_c,
            )
            if image_file:
                new_comment.image = image_file
            new_comment.save()
            post.comments += 1
            post.save()
            if post.page:
                Notification.objects.create(
                sent_to=post.user,
                sent_to_profile=post.profile,
                page = post.page,
                profile = profile,
                body = f"commented on your page {post.page.name}'s post",
                post = post
            )
            elif post.user == request.user:
                pass
            else:
                Notification.objects.create(
                    sent_to=post.user,
                    sent_to_profile=post.profile,
                    profile = profile,
                    body = "commented on your post",
                    post = post
                )
            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"

            return redirect(redirect_url)
        elif "delete_comment" in request.POST:
            post_id = request.POST.get("id")
            cid = request.POST.get("cid")
            that_post = Posts.objects.get(id=post_id)
            delete_comment = Comment.objects.get(cid=cid)
            delete_comment.delete()
            that_post.comments -= 1
            that_post.save()

            redirect_url = redirect("core:post", post_id).url
            redirect_url += "#comments"
            return redirect(redirect_url)
        elif "like_page" in request.POST:
            profile_id = request.POST.get("profile_id")
            liker_profile = Profile.objects.get(id =profile_id)
            LikedPage.objects.create(
                profile=liker_profile,
                user = request.user,
                page=page
            )
            
            page.likes +=1
            page.save()
            id = page.id
            page_url = reverse('core:page', args=[id])
            return redirect(page_url)
        elif "dislike_page" in request.POST:
            profile_id = request.POST.get("profile_id")
            dislike = LikedPage.objects.get(profile__id=profile_id)
            dislike.delete()
            page.likes -=1
            page.save()
            id = page.id
            page_url = reverse('core:page', args=[id])
            return redirect(page_url)
    context = {
        "page":page,
        "profile": profile,
        "post": post,
        "liked_post_ids":liked_post_ids,
        "liked":liked,
        "liked_by": liked_by,
    }
    return render(request, "core/page.html", context)

@login_required
def create_page(request):
    owner = Profile.objects.get(user=request.user)
    if request.method == "POST":
        name = request.POST.get("page_name")
        about = request.POST.get("about")
        profile_pic = request.FILES.get("profile_pic")
        cover_pic = request.FILES.get("cover_pic")
        new_page = Page.objects.create(
            name = name,
            about = about,
            profile_pic = profile_pic,
            cover_pic = cover_pic,
            owner = owner,
            user = owner.user
        )
        new_page.save()
        return redirect("core:page", new_page.id)
    return render(request, "core/create-page.html")

@login_required
def edit_page(request, id):
    page = Page.objects.get(id = id)
    if request.method == "POST":
        if "update_page" in request.POST:
            name = request.POST.get("page_name")
            about = request.POST.get("about")
            profile_pic = request.FILES.get("profile_pic")
            cover_pic = request.FILES.get("cover_pic")
            page.name = name
            page.about = about
            page.profile_pic = profile_pic or page.profile_pic
            page.cover_pic = cover_pic or page.cover_pic
            page.save()
            return redirect("core:page", page.id)
        elif "delete_page" in request.POST:
            page.delete()
            return redirect("core:user-pages")
    context = {
        "page": page,
    }
    return render(request, "core/edit-page.html", context)

@login_required
def user_pages(request):
    pages = None
    if Page.objects.filter(user=request.user).exists():
        pages = Page.objects.filter(user=request.user)
    if request.method == "POST":
        id = request.POST.get("id")
        page = Page.objects.get(id =id)
        page.delete()
        return redirect("core:user-pages")
    context = {
        "pages": pages,
    }
    return render(request, "core/user-pages.html", context)

@login_required
def all_users(request):
    all_users = Profile.objects.exclude(user=request.user)
    context = {
        "all_users": all_users,
    }
    return render(request, "core/all-users.html", context)

@login_required
def liked_pages(request):
    liked = None
    if LikedPage.objects.filter(user = request.user).exists():
        liked = LikedPage.objects.filter(user=request.user)
    context = {
        "liked": liked,
    }
    return render(request, "core/liked_pages.html", context)

@login_required
def all_pages(request):
    all_pages = None
    if Page.objects.all().exists():
        all_pages = Page.objects.all()
    context = {
        "all_pages": all_pages,
    }
    return render(request, "core/all_pages.html", context)

@login_required
def search(request):
    query = None
    query = request.GET.get("query")
    
    if query:
        terms = query.split()
        profile_queries = [Q(firstname__icontains=term) | Q(lastname__icontains=term) | Q(user__username__icontains=term) for term in terms]
        post_query = Q(content__icontains=query)
        page_queries = [Q(name__icontains=term) | Q(about__icontains=term) for term in terms]
        profile_results = None
        if Profile.objects.filter(*profile_queries).exists():
            profile_results = Profile.objects.filter(*profile_queries)
        post_results = None
        if Posts.objects.filter(post_query).exists():
            post_results = Posts.objects.filter(post_query)
        page_results = None
        if Page.objects.filter(*page_queries).exists():
            page_results = Page.objects.filter(*page_queries)
    
    context = {
        "profiles": profile_results,
        "pages": page_results,
        "posts": post_results,
    }
    return render(request, "core/search.html", context)

def notifications(request):
    notifications = None
    if Notification.objects.filter(sent_to=request.user).exists():
        notifications = Notification.objects.filter(sent_to=request.user).order_by("-id")
        for n in notifications:
            n.seen = True
            n.save()
    context = {
        "notifications":notifications,
    }
    return render(request, "core/notifications.html", context)