const script_tag_div = function (){

    const tag_div = document.getElementsByTagName('div');
    
    for (let i = 0; i < tag_div.length;i++){
        tag_div[i].addEventListener('click',function(e){
            if (!tag_div[i].hasAttribute('id')) {
                return 
            }
            let TAG_NAME = 'div'
            let ID = this.getAttribute("id") || ""
            let CLASS_NAME = this.getAttribute("class") || ""
            let NAME = this.getAttribute("name") || ""
            let VALUE = this.value  || ""
            let CONTENT =  ""
            let URL = this.getAttribute("href") || ""
            let TEXT = 'Nhấn div: ' + CONTENT
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

            key = ID || CLASS_NAME || VALUE || CONTENT
            if (CURRENT_URL.includes('accounts.google.com')){
                this.setAttribute('data_unique','my_id');
            }

            $.ajax({
                url: 'http://127.0.0.1:5000/',
                type:'POST',
                dataType: "json",
                data:data
            }
        )
    })
    }
};

script_tag_div();

(function() {

    let child = document.getElementsByTagName('div').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('div').length;
        if(child < newChild) {
            child = newChild;
            script_tag_div();
         }
    }, 1000);
})()
    
    