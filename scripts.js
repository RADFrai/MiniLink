$('#urlForm').submit(function(e) {
    e.preventDefault();
    let url = $('#url').val();
    $.post('/shorten', {url: url}, function(data) {
        let shortUrl = data.short_url;
        let linkElement = $('<div></div>').html('Shortened URL: <a href="/' + shortUrl + '" target="_blank">' + window.location.origin + '/' + shortUrl + '</a>');
        let statsElement = $('<p></p>').html('Visits: 0').attr('id', 'stats-' + shortUrl);
        linkElement.append(statsElement);
        $('#linksContainer').append(linkElement);
        getStats(shortUrl);
    });
});

function getStats(short_url) {
    $.get('/stats/' + short_url, function(data) {
        $('#stats-' + short_url).html('Visits: ' + data.visits);
    }).fail(function() {
        $('#stats-' + short_url).html('Visits: 0');
    });
}
