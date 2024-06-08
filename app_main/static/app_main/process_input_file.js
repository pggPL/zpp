function read_links_table(table) {
    const rows = table.getElementsByTagName("tr");
    const ret_arr = [];

    for (const elem of Array.from(rows).slice(1)) {
        let data = elem.getElementsByTagName("td");

        ret_arr.push({"platform": data[0].innerText, "link": data[1].innerText});
    }

    return ret_arr;
}

function read_all_links() {
    const post_table = document.getElementById("post-table");
    const profile_table = document.getElementById("profile-table");

    return {
        "posts": read_links_table(post_table),
        "profiles": read_links_table(profile_table)
    }
}

// Delete all nodes with specified class
function del_with_class(class_name) {
    let nodes_to_del = document.querySelectorAll("." + class_name)
    console.log(nodes_to_del);
    for (const node of nodes_to_del) {
        node.remove();
    }
}

function submit_action() {
    const links_read = read_all_links();

    fetch(confirm_add_file_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(links_read)
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Network response was not ok.")
        }
    }).then(data => {
        console.log("Success:", data);

        del_with_class("hide_after_data_added");

        const content_node = document.querySelector(".content");
        content_node.insertAdjacentHTML("beforeend", "<div> Dane zostały dodane do bazy. </div>");

    }).catch(error => {
        console.error("Error:", error);
        del_with_class("hide_after_data_added");
        const content_node = document.querySelector(".content");
        content_node.insertAdjacentHTML("beforeend","<div> Wystąpił błąd, dane nie zostały dodane. </div>");
    })

}


window.onload = function() {
    const submit_button = document.getElementById("submit-after-preview")
    submit_button.onclick = submit_action;

    const cancel_button = document.getElementById("cancel-after-preview")
    cancel_button.onclick = () => { window.location.href = add_file_url; }

}