
$(document).ready(function(){
    $('.click').click(function(e){
        var id = $(e.currentTarget).data('id');
        var id2='.container[data-id=' + id + ']';
        if($(id2).hasClass('hidden')){
        $(id2).slideDown();
        $(id2).addClass('shown');
        $(id2).removeClass('hidden');
    }
    else {
    	$(id2).slideUp();
        $(id2).addClass('hidden');
        $(id2).removeClass('shown');
    }
    });
});

