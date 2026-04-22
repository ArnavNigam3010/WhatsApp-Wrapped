let chatData = null;
let currentSlide = 0;
let userChartInstance = null; // Important: Used to prevent chart ghosting
const slides = document.querySelectorAll('.slide');
let y= new Set();
let chosen=[];
let i1=-1;
let y1=[];
let slidenum=8;

async function init() {
    try {
        const response = await fetch('data.json');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        chatData = await response.json();
        console.log("Offline Data Loaded:", chatData);

        setupBackgroundNames();
        //setupMemberSlide();
        setupGlobalStats();
        globalStats2();
        updateSlides();
        let x=setupUserGrid();
        //multiSelect();//setupUserGrid();
        
    } catch (err) {
        console.error("Initialization failed:", err);
        const title = document.querySelector('.title-hero');
        if (title) title.innerHTML = "DATA <span style='color: #ef4444'>MISSING</span>";
    }
}

function charPer(n){
    tags=[];
    for (i of ["Long Messager","Night Owl","Conversation Starter","Ghost","Hype Person","Message Editor","Emoji Talker","Long Vocabulary User"]){
        if (chatData[i]==n){
            tags.push(i);
        }
    }
    if(chatData["bestFriends"][0]==n){
        tags.push("Best Friends with "+chatData.inv_dict[chatData["bestFriends"][1]]);
    }
    if(chatData["bestFriends"][1]==n){
        tags.push("Best Friends with "+chatData.inv_dict[chatData["bestFriends"][0]]);
    }
    return tags;
}

function setupBackgroundNames() {
    const container = document.getElementById('bgNameContainer');
    if (!container) return;

    const names = Object.values(chatData.inv_dict);
    
    for (let i = 0; i < 25; i++) {
        const el = document.createElement('div');
        el.className = 'floating-name';
        el.innerText = names[i % names.length];
        
        el.style.left = Math.random() * 90 + "vw";
        el.style.top = Math.random() * 90 + "vh";
        el.style.fontSize = (2 + Math.random() * 4) + "rem";
        el.style.animationDuration = (15 + Math.random() * 15) + "s";
        el.style.animationDelay = "-" + (Math.random() * 10) + "s";
        
        container.appendChild(el);
    }
}

function setupMemberSlide(){
    let x=document.getElementById('memName')
    let content="";
    let tot = Number(chatData.length)
    for (let i=0;i<tot;i++){
        content+="<div class=\"memNames\">"+chatData.inv_dict[i]+"</div><br>"
    }
    x.innerHTML=content
}
function setupWordsChart() {
    const ctx = document.getElementById('wordsLineChart').getContext('2d');
    
    const labels = Object.values(chatData.inv_dict);
    
    const dataPoints = chatData.total_words_arr; 

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Words Used',
                data: dataPoints,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                pointBackgroundColor: '#3b82f6',
                pointRadius: 5,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}
function setupNightChart() {
    const ctx = document.getElementById('nightChart').getContext('2d');
    
    const labels = Object.values(chatData.inv_dict);
    const nightData = chatData.night_msg_arr;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Night Owl Activity (12AM - 4AM)',
                data: nightData,
                backgroundColor: 'rgba(99, 102, 241, 0.5)',
                borderColor: '#6366f1',
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: '#818cf8'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            
            plugins: {
                legend: { display: false }
            },
            
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        color: '#94a3b8'
                    }
                }
            }
        }
    });
}
function setupEditedChart() {
    const ctx = document.getElementById('editChart').getContext('2d');
    
    const labels = Object.values(chatData.inv_dict);
    
    const dataPoints = chatData.editCounter; 

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Edits',
                data: dataPoints,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                tension: 0,
                pointBackgroundColor: '#3b82f6',
                pointRadius: 5,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

function setupConvoChart() {
    const ctx = document.getElementById('convoChart').getContext('2d');
    
    const labels = Object.values(chatData.inv_dict);
    
    const dataPoints = chatData.convoStart_arr; 

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Conversations Started',
                data: dataPoints,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#3b82f6',
                pointRadius: 5,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

function setupEmojiChart() {
    const ctx = document.getElementById('emojiChart').getContext('2d');
    
    const labels = Object.values(chatData.inv_dict);
    const nightData = chatData.total_emoji_per_person;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Emojis Used',
                data: nightData,
                backgroundColor: 'rgba(99, 102, 241, 0.5)',
                borderColor: '#6366f1',
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: '#818cf8'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            
            plugins: {
                legend: { display: false }
            },
            
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        color: '#94a3b8'
                    }
                }
            }
        }
    });
}
function setupGlobalStats() {
    document.getElementById('totalMsgCount').innerText = chatData.totalMsg.toLocaleString();
    
    const memCount = document.getElementById('memCt');
    memCount.innerHTML = `
        <!--<div style="font-size: 1.2rem; color: #94a3b8; text-transform: uppercase;">Busiest Day</div>
        <div style="font-size: 1.5rem; font-weight: 700;">${chatData.busiest_day_arr}</div>-->
        <!--<div style="font-size: 1.2rem; color: #f6ff00; text-transform: uppercase;">Member Count</div>-->
        <div style="font-size: 3.5rem; font-weight: 700;">${chatData.length}</div>
    `;

    const wordCount = document.getElementById('wordCt');
    wordCount.innerHTML = `
        <div style="font-size: 3.5rem; font-weight: 700;">${chatData.totalwords.toLocaleString()}</div>
    `;

    const ctx = document.getElementById('globalActivityChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.values(chatData.inv_dict),
            datasets: [{
                data: chatData.total_messages_arr,
                backgroundColor: [
                    '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#efef44', 
                    '#6366f1', '#10b981', '#ec4899', '#06b6d4', '#8cd406'
                ],
                borderWidth: 0,
                hoverOffset: 20
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#94a3b8', font: { family: 'Calibri', size: 21 } }
                }
            }
        }
    });
}

function globalStats2(){
    //Number of People in the Chat
    //Total Messages, Total Words
    //Busiest Day, Longest Silence
    //Number of messages Edited
    setupWordsChart();
    setupNightChart();
    setupEditedChart();
    setupConvoChart();
    setupEmojiChart();
}

function setupUserGrid() {
    chosen=new Array(chatData.length).fill(false);
    const grid = document.getElementById('userGrid');
    grid.innerHTML = '';
    
    Object.keys(chatData.inv_dict).forEach((id) => {
        const name = chatData.inv_dict[id];
        const card = document.createElement('div');
        card.className = 'glass-panel';
        card.style.padding = '20px';
        card.style.cursor = 'pointer';
        card.style.textAlign = 'center';
        card.innerHTML = `
            <strong style="display: block; font-size: 1rem;">${name}</strong>
            <span class="label" style="font-size: 0.6rem;">View Stats</span>
        `;
       
        card.onclick = (e) => {
            chosen[id]=!chosen[id];
            if (chosen[id]==true){
                card.style.background="#46664c75";
                card.style["border-color"] = "#20e016b7";
                y.add(id);
                y1=[...y];
            }
            else{
                //card.style.background="rgba(255, 255, 255, 0.03)";
                //card.style["border-color"] = "rgba(255, 255, 255, 0.1)";
                card.style.background="";
                card.style["border-color"] = "";
                y.delete(id);
                y1=[...y];
            }
            e.stopPropagation(); // Prevents slide from advancing
            //showUserProfile(id);
        };
        grid.appendChild(card);
    });
    return chosen;
}

function showUserProfile(id) {//HEATMAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    const idx = parseInt(id);
    const name = chatData.inv_dict[id];
    
    fn=name.split(" ")[0]
    ln=name.split(" ")[name.split(" ").length-1]
    if (name.split(" ").length==1) ln="";
    document.getElementById('pName').innerText = name;
    document.getElementById('person').innerText = "("+charPer(idx)+")";
    document.getElementById('pInitial').innerText = fn[0]+ln[0];
    document.getElementById('pMessages').innerText = chatData.total_messages_arr[idx].toLocaleString();
    document.getElementById('pWords').innerText = chatData.total_words_arr[idx].toLocaleString();
    document.getElementById('pResponse').innerText = Math.trunc(chatData.tprsbycprs_arr[idx]/60.0 *100)/100 + "m";

    const emojiDiv = document.getElementById('pEmojis');
    emojiDiv.innerHTML = '';
    chatData.top3_emoji_arr[idx].forEach(emoji => {
        const span = document.createElement('span');
        span.className = 'glass-panel';
        span.style.padding = '10px';
        span.style.fontSize = '1.5rem';
        span.innerText = emoji;
        emojiDiv.appendChild(span);
    });

    const ctx = document.getElementById('userHourlyChart').getContext('2d');

    if (userChartInstance) {
        userChartInstance.destroy();
    }

    userChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Night Messages', 'Edits', 'Conversations Started','Emojis','Long Messages'],
            datasets: [{
                data: [
                    //chatData.total_messages_arr[idx],
                    chatData.night_msg_arr[idx],
                    chatData.editCounter[idx],
                    chatData.convoStart_arr[idx],
                    chatData.total_emoji_per_person[idx],
                    chatData.total_words_arr[idx]/chatData.total_messages_arr[idx]
                ],
                backgroundColor: ['#3b82f6', '#6366f1', '#ec4899', '#10b981', '#1eb910'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { 
                    beginAtZero: true, 
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#64748b' }
                },
                x: { ticks: { color: '#ffffff' } }
            }
        }
    });

    currentSlide=slidenum;
    renderUserHeatmap(id)
    updateSlides();
}
function renderUserHeatmap(personIdx) {
    const container = document.getElementById('heatmapGrid');
    if (!container) return;
    container.innerHTML = '';
    const totalDays = chatData.number_of_days;
    container.style.setProperty('--total-days', totalDays);

    const personData = chatData.todd[personIdx];
    if (!personData) return; 

    let maxVal = 0;
    personData.forEach(dayArray => {
        dayArray.forEach(val => { if (val > maxVal) maxVal = val; });
    });

    for (let bracketIdx = 0; bracketIdx < 12; bracketIdx++) {
        for (let dayIdx = 0; dayIdx < totalDays; dayIdx++) {
            const msgCount = personData[dayIdx][bracketIdx]; 
            const cell = document.createElement('div');
            cell.className = 'heat-cell';
            
            if (msgCount === 0 || maxVal === 0) {
                cell.classList.add('lvl-0');
            } else {
                const intensity = msgCount / maxVal;
                if (intensity < 0.25) cell.classList.add('lvl-1');
                else if (intensity < 0.50) cell.classList.add('lvl-2');
                else if (intensity < 0.75) cell.classList.add('lvl-3');
                else cell.classList.add('lvl-4');
            }

            cell.title = `Day ${dayIdx}, Time ${bracketIdx*2}-${(bracketIdx+1)*2}h: ${msgCount} msgs`;
            container.appendChild(cell);
        }
    }
}

function updateSlides() {
    slides.forEach((s, i) => {
        s.classList.toggle('active', i === currentSlide);
    });
}

document.getElementById('nextBtn').onclick = (e) => {
    e.stopPropagation();
    y1=[...y];
    if (currentSlide < slidenum) {
        currentSlide++;
        updateSlides();
    }
    if(currentSlide==slidenum){
        i1++;
        if(i1<y1.length){
            showUserProfile(y1[i1]);
        }
        else{
            currentSlide++;
            updateSlides();
        }
    }
};

document.getElementById('prevBtn').onclick = (e) => {
    e.stopPropagation();
    y1=[...y];
    if(currentSlide==slidenum){
        i1--;
        if(i1==-1){
            currentSlide--;
            updateSlides();
        }else{
            
            showUserProfile(y1[i1]);
        }
    }
    else if (currentSlide > 0) {
        currentSlide--;
        updateSlides();
        if(currentSlide==slidenum){
            if(i1==y1.length){
                i1--;
                
                if(i1==-1){
                    currentSlide--;
                    updateSlides();
                }else{
                    showUserProfile(y1[i1]);
                }
            }
        }
    }
};

// Global click to begin (Slides 0 to 1)
/*window.onclick = () => {
    if (currentSlide < 2 && chatData) {
        currentSlide++;
        updateSlides();
    }
};*/

init();