$commentInput = $('#comment-box')

$commentInput.keydown(function (e) { //Ensures characters which are not allowed in the comment box are not allowed to be inserted. 
    if (!e.key.match(/^[a-zA-Z ,.!?]+$/) || e.which == 13) {
        e.preventDefault();
    }
});