
// 선택 화면 넘기기
const steps = document.querySelectorAll(".diagnosis-step");
const nextButtons = document.querySelectorAll(".next-button");
const prevButtons = document.querySelectorAll(".prev-button");
const hobbyCheckboxes = document.querySelectorAll('input[name="hobby"]');
const diagnosisForm = document.querySelector("#diagnosisForm");
const stepIndicator = document.querySelector("#stepIndicator");
const progressFill = document.querySelector("#progressFill");
const hobbyCount = document.querySelector("#hobbyCount");
const stepTabs = document.querySelectorAll(".step-tab");
const selectedHobbyList = document.querySelector("#selectedHobbyList");
const clearHobbies = document.querySelector("#clearHobbies");
const hobbyCategoryTabs =document.querySelectorAll(".hobby-category-tab");
const hobbyCategoryGroups =document.querySelectorAll(".hobby-category-group");


// 현재 단계
let currentStep = 0;
// 정상적으로 도달한 가장 먼 단계 -> 상단바에서 이전 단계 이동 가능에 필요
let maxReachedStep = 0; 


function showStep(index){
    steps.forEach((step, stepIndex) => {
        step.hidden = stepIndex !== index;
    });

    // 진행률 변경
    stepIndicator.textContent = `STEP ${index + 1} / ${steps.length}`;

    const progress = ((index + 1) / steps.length * 100);
    progressFill.style.width = `${progress}%`;

    // 현재 단계 탭 표시
    stepTabs.forEach((tab, tabIndex) => {

        tab.classList.toggle(
            "active",
            tabIndex === index
        );

        tab.classList.toggle(
            "completed",
            tabIndex < maxReachedStep
        );

        tab.classList.toggle(
            "locked",
            tabIndex > maxReachedStep
        );
    });
}

nextButtons.forEach((button)=>{
    button.addEventListener("click", ()=>{
        if(!validateStep(currentStep)){
            return;
        }
        
        currentStep++;
        maxReachedStep = Math.max(maxReachedStep, currentStep);
        showStep(currentStep);
    });
});

prevButtons.forEach((button)=>{
    button.addEventListener("click", ()=>{
        currentStep --;
        showStep(currentStep);
    });
});

stepTabs.forEach((tab) => {
    tab.addEventListener("click", () => {

        const targetStep = Number(tab.dataset.step);

        if (targetStep > maxReachedStep) {
            return;
        }

        currentStep = targetStep;
        showStep(currentStep);
    });
});

function validateStep(index){
    // step1 : mbti
    if(index === 0){
        const selectedMbti = document.querySelector(
            'input[name="mbti"]:checked'
        );

        if(!selectedMbti){
            alert("MBTI를 선택해주세요");
            return false;
        }
    }
    
    // step3 : 목적/선호
    if(index === 2){
        const selectedPurpose = document.querySelectorAll(
            'input[name="purpose"]:checked'
        );

        const socialType = document.querySelector(
            'input[name="socialType"]:checked'
        );

        const indoorOutdoor = document.querySelector(
            'input[name="indoorOutdoor"]:checked'
        );

        const activityLevel = document.querySelector(
            'input[name="activityLevel"]:checked'
        );


        if(selectedPurpose.length === 0){
            alert("취미의 목적을 하나 이상 선택해주세요.");
            return false;
        }

        if(!socialType || !indoorOutdoor || !activityLevel){
            alert("동행, 장소, 활동량을 모두 선택해주세요.");
            return false;
        }
    }

    // step4 : 시간/예산
    if (index === 3) {
        const budgetTier = document.querySelector(
            'input[name="budgetTier"]:checked'
        );

        const timeRequired = document.querySelector(
            'input[name="timeRequired"]:checked'
        );

        if (!budgetTier || !timeRequired) {
            alert("예산과 시간을 모두 선택해주세요.");
            return false;
        }
    }

    return true;
}


// 취미 선택 검증
hobbyCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {

    const selectedHobbies = document.querySelectorAll(
      'input[name="hobby"]:checked'
    );

    if (selectedHobbies.length > 5) {
      checkbox.checked = false;
      alert("현재 취미는 최대 5개까지 선택할 수 있습니다.");
    }

    updateSelectedHobbies();

  });
});


// 상단 선택 취미 표시
function updateSelectedHobbies() {
    const selectedHobbies = document.querySelectorAll(
        'input[name="hobby"]:checked'
    );

    hobbyCount.textContent = selectedHobbies.length;

    selectedHobbyList.innerHTML = "";

    if (selectedHobbies.length === 0) {
        const emptyMessage = document.createElement("span");

        emptyMessage.className = "selected-hobby-empty";
        emptyMessage.textContent = "아직 선택한 취미가 없습니다.";

        selectedHobbyList.appendChild(emptyMessage);

        return;
    }

    selectedHobbies.forEach((checkbox) => {
        const hobbyCard = checkbox.closest(".hobby-card");

        const hobbyName = hobbyCard
            .querySelector(".hobby-name")
            .textContent
            .trim();

        const chip = document.createElement("button");

        chip.type = "button";
        chip.className = "selected-hobby-chip";
        chip.textContent = `${hobbyName} ×`;

        chip.addEventListener("click", () => {
            checkbox.checked = false;
            updateSelectedHobbies();
        });

        selectedHobbyList.appendChild(chip);
    });
}


// 취미 선택 전체 해제
clearHobbies.addEventListener("click", () => {
    hobbyCheckboxes.forEach((checkbox) => {
        checkbox.checked = false;
    });

    updateSelectedHobbies();
});


// 카테고리 클릭 기능
hobbyCategoryTabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        const selectedCategory = tab.dataset.category;

        // 선택된 탭 표시
        hobbyCategoryTabs.forEach((item) => {
            item.classList.remove("active");
        });

        tab.classList.add("active");


        // 카테고리 목록 필터
        hobbyCategoryGroups.forEach((group) => {

            if (
                selectedCategory === "all" ||
                group.dataset.category === selectedCategory
            ) {
                group.hidden = false;
            } else {
                group.hidden = true;
            }

        });

    });

});


// 폼 제출 전 예산 및 시간 선택 검증
diagnosisForm.addEventListener("submit", (event) => {
    if (!validateStep(currentStep)) {
        event.preventDefault();
    }
});

showStep(currentStep);
updateSelectedHobbies();