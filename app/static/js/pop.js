$('a[rel=popover]').popover({
    html: true,
    trigger: 'click',
    placement: 'bottom',
    content: function(){return '<img width="100%" src="'+$(this).data('img') + '" />';}
    });