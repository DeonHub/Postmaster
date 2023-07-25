// // window.onload = function() {
// //         let things = document.getElementsByTagName("input")
// //         const inputs = Array.from(things)
// //         inputs.forEach(input => {
// //                 input.addEventListener('keypress', () => {
// //                        if(input.readOnly == true){
// //                                alert("This is a readonly field")
// //                        }
// //                 })
// //         })
// //       };

// alert("Hello") 


// alert("Hello") 


const upFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}





function getData(){

        var requestOptions = {
                method: 'GET',
                redirect: 'follow'
              };

        var api_key='66d4824684db8ea0ab67fa76'
        var amount = document.getElementById('unit_amount_usd').value

        var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
                .then(response => response.json())
                .then(
                        result => {
                                // var url = result.conversion_result
                                document.getElementById('unit_amount_ghs').value = result.conversion_result
                        }
                )
                .catch(error => console.log('error', error));

}



// function getSize(){

//         var myHeaders = new Headers();
//         myHeaders.append("Content-Type", "application/json");
//         myHeaders.append("Cookie", "csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ");
//         myHeaders.append("Access-Control-Allow-Origin", "*");
        
//         var client_id = document.getElementById('client_size').value

//         // alert(client_id)

//         var raw = JSON.stringify({
//           "client_id": client_id
//         });
        
//         var requestOptions = {
//           method: 'POST',
//           headers: myHeaders,
//           body: raw,
//           redirect: 'follow'
//         };
        
//         fetch("http://127.0.0.1:8000/api/client-size/", requestOptions)
//           .then(response => response.json())
//           .then(
//                 result => {
//                         console.log(result)
//                         // document.getElementById('modula').value = result.info.membership_size
//                 }
//                 )
//           .catch(error => console.log('error', error));

// }





function addRen(){

        var inputCity1 = document.getElementById('inputCity1')
        var inputCity2 = document.getElementById('inputCity2')
        var inputZip = document.getElementById('inputZip')


        var duration = document.getElementById('duration')


        var modula = document.getElementById('modula').value
        var paymentForm = document.getElementById('paymentForm')


        // var myHeaders = new Headers();
        // myHeaders.append("Content-Type", "application/json");

        // var csrf = document.getElementByName('input[name=csrfmiddlewaretoken]').value
        // var raw = JSON.stringify({"mode":modula});


        // var requestOptions = {
        //         method: 'POST',
        //         redirect: 'follow',
        //         data: raw
        //       }


        var url = paymentForm.getAttribute("data-modula-url")

        
        // alert("Inside")

        if(duration.value == ""){
            inputCity1.value = 0 * 30
            inputZip.value = 0 - parseInt(inputCity2.value)
        }

        else{
                inputCity1.value = parseInt(duration.value) * 30
                inputZip.value = parseInt(inputCity1.value) - parseInt(inputCity2.value)
        }



        fetch(url, requestOptions)
        .then(response => response.json())
        .then(
                result => {
                        alert(result)
                        // document.getElementById('subscription_fee_usd').value = result.cost_usd * parseInt(duration.value) ? duration.value != "" : duration.value = 0
                        // document.getElementById('subscription_fee_ghs').value = result.cost_ghs * parseInt(duration.value) ? duration.value != "" : duration.value = 0
                }
        )
        .catch(error => console.log('error', error));

        
}  



const downFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}


const checkOut = (event) => {
        const expire = document.getElementById('expire')

        if(event.checked == false){
                expire.style.display = "block"
        }
        else{
                expire.style.display = "none"
        }
        
}



const getLogo = () => {

        const logo = document.getElementById('logo')
        const logoPreview = document.getElementById('logo-preview')
        const previewImage = document.querySelector(".logo-image")
        const previewTextDefault = document.querySelector(".logo-text")

        logo.addEventListener('change', function() {
                const file = this.files[0];
                
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        logoPreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        logoPreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}





function showDur(){
        dur = document.getElementById('dur')
        subscription_type = document.getElementById('subscription_type')

        
        if(subscription_type.value == "Account Activation"){
                dur.style.display= 'block';
        }
        else if(subscription_type.value == "Module Subscription"){
                dur.style.display= 'none';

        }
        else{
                dur.style.display= 'none';
        }
}


function pullDisc(source){
        disc = document.getElementById('disc')

        if (source.checked == true){
                disc.style.display = 'block';
        }
        else{
                disc.style.display = 'none';
        }
}


function toggle(source) {
        checkboxes = document.getElementsByName('foo[]');
        inputs = document.getElementsByName('foo[]');

        for(var i=0, n=checkboxes.length;i<n;i++) {
          checkboxes[i].checked = source.checked;

        //   document.getElementById("module"+i).disabled = false; 

        }
      }






const softCheck = () => {
        for(let i=1; i<100; i++){
                // let radio = document.getElementById("subject"+i)
                // let period = document.getElementById("module"+i)

                if(document.getElementById("subject"+i).checked){
                        document.getElementById("module"+i).disabled = false 

                }
                else{
                        document.getElementById("module"+i).disabled = true 
                }
                }
} 




// const radioCheck = () => {
//         for(let i=1; i<5; i++){
//                 let radio = document.getElementById("install"+i)
//                 let period = document.getElementById("period")
//                 let set_date =   document.getElementById("set_pay_date")

//                 if(radio.checked){
//                         amount.disabled = false 

//                         if(radio.value == "None"){
//                                 period.disabled = true    
//                                 set_date.disabled = false 

//                         }
//                         else{
//                                 period.placeholder = `Enter the number of ${radio.value}` 
//                                 period.disabled = false    
//                                 set_date.disabled = true       
//                         }
//                 }
//                 }
// } 

// const radioCheck2 = () => {
//         for(let i=1; i<5; i++){
//                 let radio = document.getElementById("range"+i)
//                 let period = document.getElementById("numver")

//                 if(radio.checked){
//                         period.placeholder = `Enter the number of ${radio.value} to renew for...`
//                         period.disabled = false    
//                 }
//                 }
// }


// const checkDate = () => {

//         let check = document.getElementById('check')

//         if(check.checked == true){
//                 document.getElementById("start_date").disabled = false
//                 document.getElementById("end_date").disabled = false
//         }else{
//                 document.getElementById("start_date").disabled = true
//                 document.getElementById("end_date").disabled = true 
//         }
// }


  

