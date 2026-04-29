let chatData = null;
let currentSlide = 0;
let userChartInstance = null; // stores charts
const slides = document.querySelectorAll('.slide');
let y= new Set(); // set of chosen profiles
let i1=-1; // profile index
let y1=[]; // array of chosen profiles
let slidenum=8; // slide at which profiles are shown

async function init() {
    try {
        const response = await fetch('../data.json'); // fetches json data
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        chatData = await response.json(); // stores json data

        setupBackgroundNames();
        setupGlobalStats();
        globalStats2();
        updateSlides();
        let x=setupUserGrid();
        setupBackgroundEmotions();
    } catch (err) { // Error handling
        const title = document.querySelector('.title-hero');
        if (title) title.innerHTML = "DATA <span style='color: #ef4444'>MISSING</span>";
    }
}

function charPer(n){ // assigns personality tags
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

function setupBackgroundNames() { // floating names intro page
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

function setupBackgroundEmotions() { // floating emotions last page
    const container = document.getElementById('bgEmotionsContainer');
    if (!container) return;

    const emotions = ["Memories","Friendship","Fun","Bonding","Jokes","Banter","Adventures","Gossip","Squad","Joy"];
    
    for (let i = 0; i < 25; i++) {
        const el = document.createElement('div');
        el.className = 'floating-emotions';
        el.innerText = emotions[i % emotions.length];
    
        el.style.left = Math.random() * 90 + "vw";
        el.style.top = Math.random() * 90 + "vh";
        el.style.fontSize = (2 + Math.random() * 4) + "rem";
        el.style.animationDuration = (15 + Math.random() * 15) + "s";
        el.style.animationDelay = "-" + (Math.random() * 10) + "s";
        
        container.appendChild(el);
    }
}

function setupWordsChart() { // words per person chart
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
function setupNightChart() { // night messages chart
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
function setupEditedChart() { // edited messages chart
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

function setupConvoChart() { // conversations started chart
    const ctx = document.getElementById('convoChart').getContext('2d');
    
    const labels = Object.values(chatData.inv_dict);
    
    const dataPoints = chatData.convoStart_arr; 

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: chatData.convoStart_arr,
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

function setupEmojiChart() { // emojis used chart
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
function setupGlobalStats() { // global stats (total messages, words, members, busiest day, longest silence) and messages chart 
    document.getElementById('totalMsgCount').innerText = chatData.totalMsg.toLocaleString(); // message count
    
    const memCount = document.getElementById('memCt');
    memCount.innerHTML = `${chatData.length}`; // number of members

    const wordCount = document.getElementById('wordCt');
    wordCount.innerHTML = `${chatData.totalwords.toLocaleString()}`; // word count

    const busy = document.getElementById("busyday");
    busy.innerHTML = `${chatData.busiest_day_arr}`; // busiest day

    const sil = document.getElementById("longsil");  
    sil.innerHTML = `${chatData.longest_silence/3600}h ${(chatData.longest_silence-(chatData.longest_silence/3600)*3600)/60}m ${chatData.longest_silence-(chatData.longest_silence/3600)*3600-((chatData.longest_silence-(chatData.longest_silence/3600)*3600)/60)*60}s`;
    // longest silence
    const ctx = document.getElementById('globalActivityChart').getContext('2d'); // message per person chart
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
    setupWordsChart(); // Total Words
    setupNightChart(); // night messages
    setupEditedChart(); // Number of messages Edited
    setupConvoChart(); // convostart
    setupEmojiChart(); // emojis
}

function setupUserGrid() { // for slide for choosing profiles to see
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
            e.stopPropagation();
            chosen[id]=!chosen[id];
            if (chosen[id]==true){
                card.style.background="#46664c75";
                card.style["border-color"] = "#20e016b7";
                y.add(id);
                y1=[...y];
            }
            else{
                card.style.background="";
                card.style["border-color"] = "";
                y.delete(id);
                y1=[...y];
            }
            e.stopPropagation(); // Prevents slide from advancing
        };
        grid.appendChild(card);
    });
    return chosen;
}

function showUserProfile(id) { // for individual user slides
    //HEATMAPPPPP DONE
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
    document.getElementById('pEmoji').innerText = chatData.total_emoji_per_person[idx]
    document.getElementById('pLong').innerText = chatData.longvocarray[idx]

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
            labels: ['Night Messages', 'Edits', 'Conversations Started','Long Messages'],
            datasets: [{
                data: [
                    chatData.night_msg_arr[idx],
                    chatData.editCounter[idx],
                    chatData.convoStart_arr[idx],
                    chatData.total_words_arr[idx]/chatData.total_messages_arr[idx]
                ],
                backgroundColor: ['#3b82f6', '#6366f1', '#ec4899', '#1eb910'],
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
function renderUserHeatmap(personIdx) { // to generate heatmaps
    const container = document.getElementById('heatmapGrid');
    if (!container) return;
    container.innerHTML = '';
    const totalDays = chatData.number_of_days;
    const daysShown = Math.min(70,totalDays);
    container.style.setProperty('--total-days', daysShown );

    const personData = chatData.todd[personIdx];
    if (!personData) return; 

    let maxVal = 0;
    personData.forEach(dayArray => {
        dayArray.forEach(val => { if (val > maxVal) maxVal = val; });
    });

    for (let bracketIdx = 0; bracketIdx < 12; bracketIdx++) {
        for (let dayIdx = totalDays-daysShown; dayIdx < totalDays; dayIdx++) {
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

            cell.title = `Day ${dayIdx+1}, Time ${bracketIdx*2}-${(bracketIdx+1)*2}h: ${msgCount} msgs`;
            container.appendChild(cell);
        }
    }
}

function comparisonTable(){ // comparison table for all selected users
    const tab=document.getElementById("tabledata");
    tab.innerHTML="";
    y1=[...y];
    for(let i=0;i<y1.length;i++){
        let s = `<tr>
           <td id="names">${chatData.inv_dict[y1[i]]}</td>
                                <td>${chatData.total_messages_arr[y1[i]]}</td>
                                <td>${chatData.total_words_arr[y1[i]]}</td>
                                <td>${chatData.night_msg_arr[y1[i]]}</td>
                                <td>${chatData.editCounter[y1[i]]}</td>
                                <td>${chatData.convoStart_arr[y1[i]]}</td>
                                <td>${chatData.total_emoji_per_person[y1[i]]}</td>
                            </tr>`
        tab.innerHTML+=s;
    }

}


function updateSlides() { // to update slides 
    slides.forEach((s, i) => {
        s.classList.toggle('active', i === currentSlide);
    });
}

document.getElementById('nextBtn').onclick = (e) => { // next button functionality
    e.stopPropagation();
    y1=[...y];
    if (currentSlide==9){
        document.getElementById("lastsld").innerHTML=`
            NEXT CHAT <span class="highlight">LOADING...</span>
            `;
            currentSlide++;
        updateSlides();
    }
    if (currentSlide != slidenum && currentSlide<10) {
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
            comparisonTable();
        }
    }
};

document.getElementById('prevBtn').onclick = (e) => { // back button functionality
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

document.getElementById('region-prev').addEventListener('click', () => { // for previous slide when left 1/3rd of screen is clicked
    document.getElementById('prevBtn').click();
});

document.getElementById('region-next').addEventListener('click', () => { // for next slide when right 1/3rd of screen is clicked
    document.getElementById('nextBtn').click();
});
window.addEventListener('keydown', (e) => { // right left arrow keys for navigation
    if (e.key === 'ArrowRight') {
        document.getElementById('nextBtn').click();
    } else if (e.key === 'ArrowLeft') {
        document.getElementById('prevBtn').click();
    }
});
init(); // main function call