$(document).ready(function(){
    $('.source').width($('.snippet-code').width()-40);    
});
$('body').resize(function(){
    $('.source').width($('.snippet-code').width()-40);
})