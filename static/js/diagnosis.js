
// 선택 화면 넘기기
const steps = document.querySelectorAll(".diagnosis-step");
const nextButtons = document.querySelectorAll(".next-button");
const prevButtons = document.querySelectorAll(".prev-button");
const hobbyCheckboxes = document.querySelectorAll('input[name="hobby"]');
const diagnosisForm = document.querySelector("#diagnosisForm");


let currentStep = 0;


function showStep(index){
    steps.forEach((step, stepIndex) => {
        step.hidden = stepIndex !== index;
    });
}

nextButtons.forEach((button)=>{
    button.addEventListener("click", ()=>{
        if(!validateStep(currentStep)){
            return;
        }
        
        currentStep++;
        showStep(currentStep);
    });
});

prevButtons.forEach((button)=>{
    button.addEventListener("click", ()=>{
        currentStep --;
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

    // step2 : hobby
    if(index === 1){
        const selectedHobbies = document.querySelectorAll(
            'input[name="hobby"]:checked'
        );

        if(selectedHobbies.length > 5){
            alert ("기존 취미는 최대 5개까지 선택할 수 있습니다.")
            return false;
        }
    }
    
    // step3 : 목적/선호
    if(index === 2){
        const selectedPurpose = document.querySelectorAll(
            'input[name="purpose"]:checked'
        );

        const socialType = document.querySelector(
            'select[name="socialType"]'
        ).value;

        const indoorOutdoor = document.querySelector(
            'select[name="indoorOutdoor"]'
        ).value;

        const activityLevel = document.querySelector(
            'select[name="activityLevel"]'
        ).value;


        if (selectedPurpose.length === 0) {
            alert("취미의 목적을 하나 이상 선택해주세요.");
            return false;
        }

        if (!socialType || !indoorOutdoor || !activityLevel) {
            alert("동행, 장소, 활동량을 모두 선택해주세요.");
            return false;
        }
    }

    return true;
}

// 취미 체크 박스 선택 막기
hobbyCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {

    const selectedHobbies = document.querySelectorAll(
      'input[name="hobby"]:checked'
    );

    if (selectedHobbies.length > 5) {
      checkbox.checked = false;
      alert("현재 취미는 최대 5개까지 선택할 수 있습니다.");
    }
  });
});

// 
diagnosisForm.addEventListener("submit", (event) => {

  const budgetTier =
    document.querySelector('select[name="budgetTier"]').value;

  const timeRequired =
    document.querySelector('select[name="timeRequired"]').value;

  if (!budgetTier || !timeRequired) {
    event.preventDefault();
    alert("예산과 시간을 모두 선택해주세요.");
  }
});