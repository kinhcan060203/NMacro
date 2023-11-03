var CURRENT_URL = document.location.href
console.log(CURRENT_URL)
if (!CURRENT_URL.includes('accounts.google.com')) {
    var jquery_embb = document.createElement('script');
    jquery_embb.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
    jquery_embb.id = 'myjquery';
    document.getElementsByTagName('head')[0].appendChild(jquery_embb);
}




var script_embb = document.createElement('div');
script_embb.id = 'myscript';
script_embb.hidden = 'hidden';
document.getElementsByTagName('body')[0].appendChild(script_embb);

document.addEventListener("visibilitychange", () => {
    if (document.visibilityState!=='hidden') {
        $.ajax({
            url: 'http://127.0.0.1:5000/',
            type:'POST',
            dataType: "json",
            data:JSON.stringify({'WINDOW_ID':`${window}`})
        })
    }
});

console.log("Thanhcong")
