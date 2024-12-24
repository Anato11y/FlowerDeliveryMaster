from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from orders_app.models import Flower

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews_app/list.html', {'reviews': reviews})

@login_required
def review_add(request):
    if request.method == 'POST':
        flower_id = request.POST.get('flower_id')
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        flower = Flower.objects.get(id=flower_id)
        Review.objects.create(
            user=request.user,
            flower=flower,
            text=text,
            rating=rating
        )
        return redirect('reviews:list')
    # Выбираем, к какому товару хотим оставить отзыв
    flowers = Flower.objects.all()
    return render(request, 'reviews_app/add.html', {'flowers': flowers})
