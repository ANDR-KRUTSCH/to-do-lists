window.Superlists = {};
window.Superlists.initialize = function(url = undefined) {
    $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });

    if (url) {
        $.get(url).done(function(response) {
            let rows = '';
            for (let i = 0; i < response.length; i++) {
                let item = response[i];
                rows += '\n<tr><td>' + (i+1) + ': ' + item.text + '</td></tr>';
            };
            $('#id_list_table').html(rows);
        });
    };
};