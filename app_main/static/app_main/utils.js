
function truncateString(str, max_len) {
    return str.length > max_len ? str.substring(0, max_len - 3) + "..." : str
}
function truncateLink(link) { return truncateString(link, 30); }

// Convert database date time format (ISO string) to more user friendly format
function showDate(string_date) {

    const date = new Date(string_date);

    // Formatowanie daty
    const formattedDate = date.toLocaleDateString('pl-PL', {
        weekday: 'long', // pełna nazwa dnia tygodnia
        year: 'numeric', // pełny rok
        month: 'long', // pełna nazwa miesiąca
        day: 'numeric' // dzień miesiąca
    });

    // Formatowanie czasu
    const formattedTime = date.toLocaleTimeString('pl-PL', {
        hour: '2-digit', // godzina (2 cyfry)
        minute: '2-digit', // minuty (2 cyfry)
        second: '2-digit' // sekundy (2 cyfry)
    });

    return `${formattedDate} ${formattedTime}`

}

