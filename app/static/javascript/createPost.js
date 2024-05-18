//Image preview

$(document).ready(function () {
    $('#file-upload').change(function (event) {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#img-preview').attr('src', e.target.result).css('display', 'block');
            };
            reader.readAsDataURL(input.files[0]);
        }
    });
});

//Tag addition

let $input = $('#tag-text-input');
let $tagForm = $('#tag-div');
let $output = $('.tags');
let $hiddenTags = $('#hidden-tags');
let $captionForm = $('#caption-text-input');

function updateHiddenTags() {
    let tags = [];
    $output.children('.tag').each(function () {
        let tagText = $(this).text().replace('close', '').trim();
        tags.push(tagText);
    });
    $hiddenTags.val(tags.join(','));
}

function outputTag() {
    const tag = `
    <span class="tag">
        <b>${$input.val()}</b>
        <span class="material-symbols-outlined remove-btn">
            close
        </span>
    </span>
    `;

    $output.append(tag);
    $input.val("");
    updateHiddenTags();
}

$tagForm.keydown(function (e) { //Event listener on the enter button to see if a tag has been submitted
    if (!e.key.match(/^[a-zA-Z]+$/)) {  
        e.preventDefault();
    }

    else if (e.which == 13) {
        e.preventDefault();
        let empty = $input.val() === "" ? true : false;
        
        if ($output.children().length >= 4 && !empty) {
            outputTag();
            $input.prop('disabled', true);
            $input.val("");
            $input.attr('placeholder', "Max number of tags reached!");
        }
        else if (!empty) {
            outputTag();
        }
    }
});

$captionForm.keydown(function (e) { //Ensures characters which are not allowed in the caption are not allowed to be inserted. 
    if (!e.key.match(/^[a-zA-Z ,.!?]+$/) || e.which == 13) {
        e.preventDefault();
    }
});

$(window).on('click', function (e) { //Event listener on window (and if on remove button), removes tags and allow for a new one to be made
    if (e.target.classList.contains('remove-btn')) {
        e.target.parentElement.remove();
        $input.prop('disabled', false);
        $input.attr('placeholder', "Press enter to add a tag...");
    }
})
