
function truncateString(str, max_len) {
    return str.length > max_len ? str.substring(0, max_len - 3) + "..." : str
}
function truncateLink(link) { return truncateString(link, 30); }

// Convert database date time format (ISO string) to more user friendly format
function showDate(string_date) {

    const date = new Date(string_date);

    const formattedDate = date.toLocaleDateString('pl-PL', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    const formattedTime = date.toLocaleTimeString('pl-PL', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    return `${formattedDate} ${formattedTime}`

}

function isTiktokVideo(url) {
    const tiktok_video_regex = /^.*https:\/\/(?:m|www|vm)?\.?tiktok\.com\/(.*\b(?:(?:usr|v|embed|user|video)\/|\?shareId=|&item_id=)(\d+)|\w+)/;
    return tiktok_video_regex.test(url);
}

