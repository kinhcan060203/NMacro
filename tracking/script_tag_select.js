
const script_tag_select = function () {


    const tag_select = document.getElementsByTagName('select');

    for (let i = 0; i < tag_select.length;i++){

        tag_select[i].addEventListener('change',function(e){
            let TAG_NAME = 'select'
            let ID = this.getAttribute("id") || ""
            let CLASS_NAME = this.getAttribute("class") || ""
            let NAME = this.getAttribute("name") || ""
            let VALUE = this.value  || ""
            let CONTENT = this.textContent.replace(/[\\n\\t\\r]/g,"") || ""
            let URL = this.getAttribute("href") || ""
            let TEXT = 'Chọn: '+this.options[this.selectedIndex].text.toLowerCase() 
            let EVENT = 'click'
            let CURRENT_URL = document.location.href
            let HOST_URL = document.location.origin
            if (URL && !URL.includes('http')){
                URL = HOST_URL + URL
            }
            let data  = {
                TAG_NAME:TAG_NAME,
                ID:ID,
                CLASS_NAME:CLASS_NAME,
                NAME:NAME,
                VALUE:VALUE,
                CONTENT:CONTENT,
                TEXT:TEXT,
                EVENT:EVENT,
            }

            data = JSON.stringify({'URL':URL, 'ACTION':data, 'WINDOW_ID':`${window}`,'CURRENT_URL':CURRENT_URL});

            if (CURRENT_URL.includes('accounts.google.com')){
                this.setAttribute('data_unique','my_id');
            }

            $.ajax({
                url: 'http://127.0.0.1:5000/',
                type:'POST',
                dataType: "json",
                data:data
            })
        })
    }
};

script_tag_select();


(function() {

    let child = document.getElementsByTagName('select').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('select').length;
        if(child < newChild) {
            child = newChild;
            script_tag_select();
         }
    }, 1000);
})()
