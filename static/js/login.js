const validUsers = [
    { name: "Zunaira Tariq", code: "TVET-2026-12345", year:"Final Year"},
    { name: "Ali Khan", code: "TVET-2026-54321", year:"FYP"}
];

document.getElementById("loginForm").addEventListener("submit", function(e){
    e.preventDefault();

    const name=document.getElementById("name").value.trim();
    const code=document.getElementById("code").value.trim();
    const year=document.querySelector('input[name="year"]:checked');

    if(!year){
        document.getElementById("errorMsg").textContent="Select year";
        return;
    }

    const user=validUsers.find(u=>u.name===name && u.code===code && u.year===year.value);

    if(user){
        alert("Login Successful");
        window.location.href="test.html";
    }else{
        document.getElementById("errorMsg").textContent="Invalid details";
    }
});