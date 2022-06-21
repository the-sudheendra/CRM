
let sinup=document.querySelector(".sign-up-btn");
let forgot=document.querySelector(".forgot");
let input_fields_up=document.querySelector(".input-fields");
let signup_fields=document.querySelector(".signup-fields");

let input_fields_in=document.querySelector(".login-btn");
console.log(forgot);
sinup.addEventListener("click",()=>
{
    input_fields_up.style.display="none";
    signup_fields.style.display="block";
    forgot.style.display="none";
    sinup.style.background="rgb(77, 121, 255)";
    input_fields_in.style.background="none";
    input_fields_in.style.color="black"
 });
input_fields_in.addEventListener("click",()=>
{
    input_fields_up.style.display="block";
    signup_fields.style.display="none";
    forgot.style.display="block";
    sinup.style.background="none";
    input_fields_in.style.background="rgb(77, 121, 255)";

});
//--------------------------------------------------------------------------------- start validate pass-----------------

let signup_pass_1=document.querySelector(".input-element-1");
let error_msg=document.querySelector(".error-msg");
let signup_pass_2=document.querySelector(".input-element-2");


// validate password
function validate()
{
    x=signup_pass_1.value;
    
   if(isok(x))
    {
        signup_pass_1.style.borderColor="green"; 
    }
    else
    {
        signup_pass_1.style.borderColor="red"; 
    }

}
function isok(x)
    { 
   // console.log("45")
    let c=0;
if(!lengthThere(x))
{
    error_msg.style.display="block";
    error_msg.innerHTML="{8 Character}";
    error_msg.style.color="red";
    document.querySelector("#NONE").classList.add("none");
    return false;

}




        error_msg.style.display="none";


        document.querySelector("#NONE").classList.remove("none");
        return true;
       

}
function lengthThere(x)
{
if(x.length>=8)
return true;
return false;
}
function upperThere(x)
{
for(let i=0;i<x.length;i++)
{
if(x.charCodeAt(i)>=65 && x.charCodeAt(i)<=90)
{
    
    return true;
}
}
return false;
}

 //--------------------------------------------------------------------------------- complete validate pass-----------------
//---------------------------------------------------------------------------------- start re-enter pass--------------------

function isSame()
{
    let x=signup_pass_2.value;
    let y=signup_pass_1.value;
    if(y.length>0 && x.length>0)
    if(!(x===y))
    {
        error_msg.style.display="block";
        error_msg.innerHTML="Not Matched";
        console.log("bye");

       
        
    }
    else
    {

    error_msg.style.display="none";
        document.querySelector("#NONE-2").classList.remove("none");
    }

}
