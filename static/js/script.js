//Show and hide map
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
})

$(document).ready(function(){
    $("#flip").click(function(){
        $("#panel").slideToggle("slow");
    });
});

//Show image original size
$('.member_img').on('click','#enlarge', function(){
    window.open($(this).attr('src'));
});