from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Review

@login_required
def add_review_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating:
            errors['rating'] = "Rating is required."
        if not comment:
            errors['comment'] = "Comment is required."

        if not errors:
            Review.objects.create(
                product=product,
                customer=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Review added successfully.")
            return redirect(f'/products/{product.id}/')
        
    return render(request, 'main/add_review_page.html', {'product': product, 'errors': errors})