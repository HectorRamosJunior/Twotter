$(document).ready(function() {
    var $twoot_text = $("#twoot_text");
    var $twoot_button = $("#twoot_button");
    var $twoot_character_count = $("#twoot_character_count");

    // On first click and first click only, remove 140 character here text
    var click_count = 0;
    $twoot_text.click(function(){
        if (click_count === 0) {
            $twoot_text.empty();  
        }
        click_count++;
    });

    // If someone is getting close to 140 char limit, show them characters left
    // If someone exceeds the character limit, disable the submit button.
    $twoot_text.bind("DOMSubtreeModified", function(){
        var characters_left = 140 - $twoot_text.text().length

        // Handle if incorrect number of characters
        if (characters_left < 0 || characters_left === 140){
            $twoot_button.prop("disabled", true);

            if (characters_left < 0){
                $twoot_character_count.css("color", "red")
                $twoot_character_count.text(characters_left);
            }
        }
        // Handle correct number of characters in form
        else{
            $twoot_button.prop("disabled", false);

            if (characters_left <= 20){
                $twoot_character_count.css("color", "black")
                $twoot_character_count.text(characters_left);
            }
            else if (characters_left > 20){
                $twoot_character_count.empty();
            }  
        }
    });

    $twoot_button.click(function(){
        // Ajax call to upload the score to the website's backend
        $.ajax({
            url : "make_twoot/",
            type : "POST", // http method
            data : { twoot_text : $twoot_text.text(), csrfmiddlewaretoken: window.CSRF_TOKEN },

            // handle a successful response
            success : function(json) {
              console.log("Worked!")
              //add_twoot_to_index();
              location.reload()
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
              console.log("Failed!")
            }
        });

        $twoot_text.empty();
    });

});