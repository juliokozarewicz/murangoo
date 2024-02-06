window.sessionStorage.clear();
window.sessionStorage.setItem('status_menu', 'menu_off');


/* chat init */
function status_chat() {

    try {

        this.chat_status = window.sessionStorage.getItem('chat_status')

        if (this.chat_status === 'chat_on') {

            this.chat_status = window.sessionStorage.setItem('chat_status', 'chat_off')

            // ======================================================================
            document.getElementById('id-chat-load').style.display = "none";
            document.getElementById('id-chat-icon').src = "../static/core/images/chat.svg"
            // ======================================================================

        } else if (this.chat_status === 'chat_off') {

            this.chat_status = window.sessionStorage.setItem('chat_status', 'chat_on')

            // ======================================================================
            document.getElementById('id-chat-load').style.display = "block";
            document.getElementById('id-chat-icon').src = "../static/core/images/close-chat.svg"
            // ======================================================================

        } else if (this.chat_status === null) {

            this.chat_status = window.sessionStorage.setItem('chat_status', 'chat_on')

            // ======================================================================
            document.getElementById('id-chat-load').style.display = "block";
            document.getElementById('id-chat-icon').src = "../static/core/images/close-chat.svg"
            // ======================================================================

        }

    } catch (error) {
        console.log('***** [ ERROR - STATUS CHAT ! ] *****')
        console.log(error)
    }

}
/* chat end */

/* change url browser init */
function changeurlnoupdate(urlstr) {

    history.pushState({}, null, urlstr);

}
/* change url browser end */

/* unload page init */
function unloadPage(pg_unload) {

    var element = document.getElementById(pg_unload);

    element.style.display = "none";

}
/* unload page end */

/* menu init */
function status_menu() {

    try {

        this.status_menu = window.sessionStorage.getItem('status_menu');

        if (this.status_menu === 'menu_on') {

            /* FRAME ALL ANIMATION */
            document.getElementById('idblackbackground').style="display: none;";
            document.getElementById('idbackgroundred').style="-webkit-animation: closeredbarmenu 0.5s forwards;";

            /* HAMBURGUER ANIMATION */
            document.getElementById('linemenuhamb1').style="-webkit-animation: menuhambine1close 0.5s forwards;";
            document.getElementById('linemenuhamb2').style="-webkit-animation: menuhambine2close 0.3s forwards;";
            document.getElementById('linemenuhamb3').style="-webkit-animation: menuhambine3close 0.5s forwards;";
            document.getElementById('idmenuhambsquare').style="position: relative;"

            /* HIDE CONTENT */
            document.getElementById('idmenuhamboptions').style="display: none;";
            document.getElementById('idloginmenuhambbottombtn').style="display: none;";

            /* UNBLOCK SCROLL */
            window.onscroll = function () { window.scrollTo(); };

            /* SET STATUS */
            this.status_menu = window.sessionStorage.setItem('status_menu', 'menu_off');

        } else if (this.status_menu === 'menu_off') {

            /* FRAME ALL ANIMATION */
            document.getElementById('idblackbackground').style="display: flex;";
            document.getElementById('idbackgroundred').style="-webkit-animation: openredbar 0.5s forwards;";

            /* HAMBURGUER ANIMATION */
            document.getElementById('linemenuhamb1').style="-webkit-animation: menuhambine1open 0.5s forwards;";
            document.getElementById('linemenuhamb2').style="-webkit-animation: menuhambine2open 0.3s forwards;";
            document.getElementById('linemenuhamb3').style="-webkit-animation: menuhambine3open 0.5s forwards;";
            document.getElementById('idmenuhambsquare').style="position: fixed; top: 2vh; right: 0vh;"
            
            /* SHOW CONTENT */
            setTimeout(function() {
                document.getElementById('idmenuhamboptions').style="display: block;";
                document.getElementById('idloginmenuhambbottombtn').style="display: flex;";
            }, 600);

            /* BLOCK SCROLL */
            window.onscroll = function () {
                window.scrollTo(0, 0);
            };

            /* SET STATUS */
            this.status_menu = window.sessionStorage.setItem('status_menu', 'menu_on');
        }

    } catch (error) {

        console.log('***** [ ERROR - STATUS MENU ! ] *****')
        console.log(error) 

    }

}
/* menu end */

/* unload page init */
function unloadPage(pg_unload) {

    var element = document.getElementById(pg_unload);

    element.style.display = "none";

}
/* unload page end */

/* cookies message init */
function cookiesmessage() {

    var status_cookieMessage = document.cookie.replace(/(?:(?:^|.*;\s*)statusCookiemessage\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    if (status_cookieMessage === 'statusCookiemessageOPEN' || status_cookieMessage === "") {

        // set status cookie
        document.cookie = "statusCookiemessage=statusCookiemessageCLOSED; path=/; SameSite=Strict;";
        
        // hide content
        document.getElementById('allcookiesdivison').style.display = 'none';

    }

}
/* cookies message end */