const script_tag_button = function (){

    const tag_button = document.getElementsByTagName('button');
    const tag_exp= ['img','span','div','svg','path','form']
    for (let i = 0; i < tag_button.length;i++){
        tag_button[i].addEventListener('click',function(e){

            number_of_child = tag_button[i].getElementsByTagName('*').length
            for (tag of tag_exp){
                number_of_child -= tag_button[i].getElementsByTagName(tag).length;
            }
            if (number_of_child > 0 ){
                return 
            }
            let TAG_NAME = 'button'
            let ID = this.getAttribute("id") || ""
            let CLASS_NAME = this.getAttribute("class") || ""
            let NAME = this.getAttribute("name") || ""
            let VALUE = this.value  || ""
            let CONTENT = this.innerText || ""
            let URL = this.getAttribute("href") || ""
            let TEXT = 'Nhấn nút: ' + CONTENT
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

script_tag_button();

(function() {

    let child = document.getElementsByTagName('button').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('button').length;
        if(child < newChild) {
            child = newChild;
            script_tag_button();
         }
    }, 1000);
})()
    
    