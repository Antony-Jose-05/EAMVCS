let mediaRecorder;
let recordedChunks = [];
let recordedBlob = null;

async function startRecording() {
  const status = document.getElementById("recordingStatus");

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    recordedChunks = [];

    mediaRecorder.ondataavailable = e => recordedChunks.push(e.data);

    mediaRecorder.onstop = () => {
      recordedBlob = new Blob(recordedChunks, { type: "audio/wav" });
      status.innerText = "Recording ready ✔️";
    };

    mediaRecorder.start();
    status.innerText = "Recording...";
  } catch {
    alert("Microphone access denied");
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

async function generate() {
  const text = document.getElementById("text").value;
  const language = document.getElementById("language").value;
  const uploadedAudio = document.getElementById("audio").files[0];

  if (text.trim() === "") {
    alert("Please enter text");
    return;
  }

  // Reference voice is mandatory
  if (!uploadedAudio && !recordedBlob) {
    alert("Please upload or record a reference voice");
    return;
  }

  const formData = new FormData();
  formData.append("text", text);
  formData.append("language", language);

  if (uploadedAudio) {
    formData.append("audio", uploadedAudio);
  } else {
    formData.append("audio", recordedBlob, "recorded.wav");
  }

  try {
    const response = await fetch("http://localhost:5000/generate", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error();

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    document.getElementById("player").src = url;
    document.getElementById("download").href = url;
  } catch {
    alert("Backend not connected");
  }
}
