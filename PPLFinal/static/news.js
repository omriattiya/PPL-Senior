let socket = null;

let button_is_stop_mode = true;

function stop_load() {
    let button = document.getElementById('stop_load');
    if (button_is_stop_mode) {
        button_is_stop_mode = false;
        socket.emit('stop');
        button.innerText = "Restart Loading Content " + String.fromCharCode(10226)
    } else {
        button_is_stop_mode = true;
        location.reload();
    }

}

window.onload = function () {
    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit('connected', {data: 'I\'m connected!'});
    });

    socket.on('add news', function (news) {
        let div_news = document.getElementById('news');

        let child_div = document.createElement('div');

        let hr = document.createElement('hr');

        let image = document.createElement('img');
        image.alt = news['title'];
        image.src = news['thumbnail'];
        image.setAttribute('width', '30%');

        let text_div = document.createElement('div');
        text_div.className = 'news_title';
        let header_title = document.createElement('h4');
        header_title.innerText = news['title'];
        let header_abstract = document.createElement('h6');
        header_abstract.innerText = news['abstract'];
        text_div.appendChild(header_title);
        if (news['thumbnail'] !== '')
            text_div.appendChild(image);
        text_div.appendChild(header_abstract);

        let link = document.createElement('a');
        link.href = news['url'];
        link.text = link.href;
        link.className = 'news-link';
        link.target = "_blank";
        link.rel = "noopener noreferrer";

        child_div.appendChild(text_div);
        child_div.appendChild(link);
        child_div.appendChild(hr);

        div_news.appendChild(child_div);
    });
};


window.onscroll = function () {
    scrollFunction()
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("myBtn").style.display = "block";
    } else {
        document.getElementById("myBtn").style.display = "none";
    }
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}