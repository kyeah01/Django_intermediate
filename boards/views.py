from django.shortcuts import render, redirect
from .models import Board, Comment

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {
        'boards' : boards,
    }
    return render(request, 'boards/index.html', context)
    
def new(request):
    # create 방식
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        board = Board(title=title, content=content)
        board.save()
        return redirect('boards:detail', board.pk)
    else:
        return render(request, 'boards/new.html')
    
def detail(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    comments = board.comment_set.all()
    context = {
        'board' : board,
        'comments' : comments,
    }
    return render(request, 'boards/detail.html', context)
    
def delete(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect('boards:detail', board.pk)
    
def edit(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    if request.method == "POST":
        board.title = request.POST.get('title')
        board.content = request.POST.get('content')
        board.save()
        return redirect('boards:detail', board.pk)
    else:
        context = {
            'board' : board
        }
        return render(request, 'boards/edit.html', context)
        
def comments_create(request, board_pk):
    # 댓글을 달 게시물을 먼저 가져와야 함.
    board = Board.objects.get(pk=board_pk)
    # form에서 넘어온 comment data
    content = request.POST.get('content')
    # 이제 댓글을 생성하고 저장하면 됨.
    # board자체를 할당하는건 
    comment = Comment(board=board, content=content)
    comment.save()
    return redirect('boards:detail', board.pk)
    
def comments_delete(request, board_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        comment.delete()
    return redirect('boards:detail', board_pk)