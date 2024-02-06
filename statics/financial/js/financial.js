window.sessionStorage.setItem('status_menu', 'menu_off');
window.sessionStorage.setItem('status_account', 'account_off');



/* menu init */
function status_menu() {

    try {

        this.status_menu = window.sessionStorage.getItem('status_menu');

        if (this.status_menu === 'menu_on') {

            /* FRAME ALL ANIMATION */
            document.getElementById('idhamboptionsmenu').style = 'display: none;';
            document.getElementById('idredbackgorund').style="-webkit-animation: blackbackgroundclose 0.3s forwards;";
            document.getElementById('idblackbackgroundhamb').style = 'display: none;';

            document.getElementById('idmenurightkebab').style="z-index: 100;"

            /* HAMBURGUER ANIMATION */
            document.getElementById('idhamb1').style="-webkit-animation: idhamb1back 0.2s forwards;";
            document.getElementById('idhamb2').style="-webkit-animation: idhamb2back 0.1s forwards;";
            document.getElementById('idhamb3').style="-webkit-animation: idhamb3back 0.2s forwards;";
            document.getElementById('idclcickmenulefthamburguer').style.position = 'relative' 

            /* UNBLOCK SCROLL */
            window.onscroll = function () { window.scrollTo(); };

            /* SET STATUS */
            this.status_menu = window.sessionStorage.setItem('status_menu', 'menu_off');

        } else if (this.status_menu === 'menu_off') {

            this.status_account = window.sessionStorage.getItem('status_account');

            if (this.status_account === 'account_on') {
                new status_account();
            }

            document.getElementById('idmenurightkebab').style="z-index: 85;"

            /* FRAME ALL ANIMATION */
            document.getElementById('idblackbackgroundhamb').style = 'display: flex;';
            document.getElementById('idredbackgorund').style="-webkit-animation: blackbackgroundgrowth 0.3s forwards;";

            /* HAMBURGUER ANIMATION */
            document.getElementById('idhamb1').style="-webkit-animation: idhamb1growth 0.2s forwards;";
            document.getElementById('idhamb2').style="-webkit-animation: idhamb2growth 0.1s forwards;";
            document.getElementById('idhamb3').style="-webkit-animation: idhamb3growth 0.2s forwards;";
            document.getElementById('idclcickmenulefthamburguer').style.position = 'absolute' 

            /* BLOCK SCROLL */
            window.onscroll = function () {
                window.scrollTo(0, 0);
            };

            /* SHOW CONTENT */
            setTimeout(function() {
                document.getElementById('idhamboptionsmenu').style = 'display: flex;';
            }, 300);

            /* SET STATUS */
            this.status_menu = window.sessionStorage.setItem('status_menu', 'menu_on');
        }

    } catch (error) {

        console.log('***** [ ERROR - STATUS MENU ! ] *****')
        console.log(error)

    }

}
/* menu end */

/* ACCOUNT init */
function status_account() {

    try {

        this.status_account = window.sessionStorage.getItem('status_account');

        if (this.status_account === 'account_on') {

            /* HIDE CONTENT */
            document.getElementById('idblackbackgroundkebab').style = 'display: none;';
            document.getElementById('idmenuoptionskebab').style = 'display: none;';
            document.getElementById('idlogout').style = 'display: none;';

            document.getElementById('idclcickmenulefthamburguer').style="z-index: 100;"
            document.getElementById('idaccountball').style = 'background-color: var(--black);';
            document.getElementById('textinitialsbasebar').textContent = document.getElementById('textinitialsbasebar').getAttribute('data-user-initials');

            /* UNBLOCK SCROLL */
            window.onscroll = function () { window.scrollTo(); };

            /* SET STATUS */
            this.status_account = window.sessionStorage.setItem('status_account', 'account_off');

        } else if (this.status_account === 'account_off') {

            this.status_menu = window.sessionStorage.getItem('status_menu');

            if (this.status_menu === 'menu_on') {
                new status_menu();
            }

            /* SHOW CONTENT */
            document.getElementById('idblackbackgroundkebab').style = 'display: flex;';
            document.getElementById('idmenuoptionskebab').style = 'display: flex;';
            document.getElementById('idlogout').style = 'display: flex;';

            document.getElementById('idclcickmenulefthamburguer').style="z-index: 85;";
            document.getElementById('idaccountball').style = 'background-color: var(--red);';
            document.getElementById('textinitialsbasebar').textContent = 'X';

            /* BLOCK SCROLL */
            window.onscroll = function () {
                window.scrollTo(0, 0);
            };

            /* SET STATUS */
            this.status_account = window.sessionStorage.setItem('status_account', 'account_on');
        }

    } catch (error) {

        console.log('***** [ ERROR - STATUS MENU ! ] *****')
        console.log(error)

    }

}
/* ACCOUNT end */

/* unload page init */
function unloadPage(pg_unload) {

    var element = document.getElementById(pg_unload);

    element.style.display = "none";

}
/* unload page end */

/* unload page init */
function loadPage(pg_load, id_replaced) {
    var pg_load = pg_load
    var id_replaced = id_replaced
    var url = '' + pg_load + ''

    var xml = new XMLHttpRequest()

    document.getElementById(id_replaced).style = "display: flex;"

    xml.onreadystatechange = function () {

        if (xml.readyState == 4 && xml.status == 200) {

            document.getElementById(id_replaced).innerHTML = xml.responseText

        }

    }

    xml.open("GET", url, true)

    xml.send()

}
/* unload page end */

// send form filter (init)
function sendforms(idform) {
    document.getElementById(idform).submit();
}
// send form filter (end)

// Copy invoice (INIT)
function fill_out_copy_form(
    posting_type,
    id_payment_description,
    id_payment_amount,
    id_due_date,
    id_category,
    id_bank_account,
    id_payee,
    id_document_number,
    id_card,
    id_notes
) {
    var formulario = document.getElementById('forminsertinvoice_new');

    // clean id payment amount
    var new_id_payment_amount = id_payment_amount.replace(/,/g, '.');

    // clean due date
    //var dateParts = id_due_date.split('-');
    //var new_id_due_date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]).toLocaleDateString();

    formulario.elements['posting_type'].value = posting_type;
    formulario.elements['id_payment_description'].value = id_payment_description;
    formulario.elements['id_payment_amount'].value = new_id_payment_amount;
    formulario.elements['id_due_date'].value = id_due_date;
    formulario.elements['id_category'].value = id_category;
    formulario.elements['id_bank_account'].value = id_bank_account;
    formulario.elements['id_payee'].value = id_payee;
    formulario.elements['id_document_number'].value = id_document_number;
    formulario.elements['id_card'].value = id_card;
    formulario.elements['id_notes'].value = id_notes;
}
// Copy invoice (END)


document.body.addEventListener("wheel", e=>{
    if(e.ctrlKey)
      e.preventDefault();
  });