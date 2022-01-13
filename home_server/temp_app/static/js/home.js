import * as THREE from "../moduleLibs/build/three.module.js";
import { FontLoader } from '../moduleLibs/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from '../moduleLibs/examples/jsm/geometries/TextGeometry.js';

const degreeNum = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30];
const humidiNum = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
/* global THREE */
"use strict";
// * Initialize webGL
const canvas = document.getElementById('myCanvas');
const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true
});
renderer.setClearColor('#3c3a3a');    // set background color
const sizeSettingsButton = 0;
renderer.setSize(window.innerWidth / 1.45, window.innerHeight / 1.5);

//const data1 = {date: [12,13,14,15,16,17,18,19,20,21,22],
//                degree:[14.3,15.3,21.1,22,22.3,22.4,25,25.6,25,18.6,17],
//              humidity:[50.3,40.3,37.4,40,53.6,60.5,60,61.2,63,64.5,50]}

// Create a new Three.js scene with camera and light
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, canvas.width / canvas.height,
  1, 500);
camera.position.set(0, 0, 100); // Set position like this
camera.lookAt(new THREE.Vector3(0, 0, 0))
const ambientLight = new THREE.AmbientLight(0x0e0e0e); // soft white light
scene.add(ambientLight);
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();



// get data from database
let localData = [[], [], [], [], [], [], [], [], [], []];
let minTimeStamp = Infinity;
let maxTimeStamp = 0;
const sensorData = JSON.parse(load_sensors());
const outData = JSON.parse(load_outData());
let localWether = [];
for (let i = 0; i < outData.length; i++) {
  const timestamp = (new Date(outData[i].fields.timestamp).getTime() / 1000);
  outData[i].fields.timestamp = timestamp;
  if (timestamp > maxTimeStamp) maxTimeStamp = timestamp;
  if (timestamp < minTimeStamp) minTimeStamp = timestamp;
}

const datas = JSON.parse(load_data());
for (let i = 0; i < datas.length; i++) {
  if (datas[i].fields.sensor != null) {
    localData[datas[i].fields.sensor - 1].push(datas[i].fields);
    const timestamp = (new Date(localData[datas[i].fields.sensor - 1][localData[datas[i].fields.sensor - 1].length - 1].timestamp).getTime() / 1000)
    localData[datas[i].fields.sensor - 1][localData[datas[i].fields.sensor - 1].length - 1].timestamp = timestamp;
    if (timestamp > maxTimeStamp) maxTimeStamp = timestamp;
    if (timestamp < minTimeStamp) minTimeStamp = timestamp;

  }
}


const defaultMaxTimeStamp = maxTimeStamp;
const defaultMinTimeStamp = minTimeStamp;
let NumOfData = outData.length;
for (var i = 0; i < localData.length; i++) {
  if (localData[i].length > NumOfData) {
    NumOfData = localData[i].length;
  }
}
let shownData = NumOfData;

// interrupts
document.addEventListener('mousemove', onDocumentMouseMove, false);
window.addEventListener('resize', onWindowResize, false);
document.addEventListener('mousedown', onMouseDown, false);

const diagram = new THREE.Object3D();
let width = (window.innerWidth / 1.45) / 9;
let height = (window.innerHeight / 1.5) / 9;

diagram.position.set(-width / 2, -height / 2, 0);
scene.add(diagram)
const loader = new FontLoader();

// initialize variables
const material = new THREE.LineBasicMaterial({ color: 0x000000 });
const dashedMat = new THREE.LineDashedMaterial({ color: 0xd0d0d0 });
const lineColor = [0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0xFF00FF, 0x00FFFF];
const humColor = [0xFF9090, 0x9090FF, 0x90FF90, 0xFFFF90, 0xFF90FF, 0x90FFFF];
const weatherMat = new THREE.LineBasicMaterial({ color: 0x000000 });
const weatherHumMat = new THREE.LineBasicMaterial({ color: 0xd0d0d0 });
let dashedPoints = [2];
let points = [3];
let scalePointsX = [2];
let scalePointsY = [2];
let scalePointsY2 = [2];
const start = 1;
let dataStart = 0;
let scaleXLine = 0;
let scaleYLine = 0;
let scaleY2Line = 0;
let dataPoints = [];
let dataHumPoints = [];
let dataLine = [];
let dataHumLine = [];
let weatherPoints = [];
let weatherHumPoints = [];
let weatherLine = [];
let weatherHumLine = [];
const tempText = [];
const humText = [];
const clk = new THREE.Clock();
const h = clk.getDelta();
const t = clk.getElapsedTime();

drawLegend()
createText();
drawStatic();
drawData()
render();
renderer.render(scene, camera);


function render() {
  renderer.render(scene, camera);
}


// mouse move interrupt handler
function onDocumentMouseMove(event) {
  event.preventDefault();
  mouse.x = (event.clientX / (window.innerWidth));
  mouse.y = (event.clientY / (window.innerHeight));

  // changes data to show
  const d = defaultMaxTimeStamp - defaultMinTimeStamp;
  maxTimeStamp = defaultMaxTimeStamp - (d * mouse.y * 0.9);
  minTimeStamp = defaultMinTimeStamp + (mouse.x * d)
  const newD = maxTimeStamp - minTimeStamp;
  maxTimeStamp = maxTimeStamp + (mouse.x * d);
  drawData();
  render();
}

// window resize handler
function onWindowResize() {
  camera.aspect = (window.innerWidth / 1.45) / (window.innerHeight / 1.5);
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth / 1.45, window.innerHeight / 1.5);
  width = (window.innerWidth / 1.45) / 9;
  height = (window.innerHeight / 1.5) / 9;
  drawStatic();
  drawData();
  render();

}
/*
function manageRaycasterIntersections(scene, camera) {
    camera.updateMatrixWorld();
    raycaster.setFromCamera(mouse, camera);
    var intersects = raycaster.intersectObjects(scene.children);

    if (intersects.length > 0) {

    }
    else {

    }
}
*/
function onMouseDown(event) {

}

// create the text of y-axis
function createText() {

  const tempTextMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
  const humTextMat = new THREE.MeshBasicMaterial({ color: 0xd0d0d0 });
  loader.load('static/moduleLibs/examples/fonts/droid/droid_sans_mono_regular.typeface.json', function (font) {
    for (let i = 0; i < degreeNum.length; i++) {
      const tempTextGeo = new TextGeometry(degreeNum[i].toString() + '°C', {
        font: font,
        size: 1.5,
        height: 0,
        curveSegments: 4,
        bevelEnabled: false,
        bevelThickness: 10,
        bevelSize: 1,
        bevelOffset: 0,
        bevelSegments: 1
      });
      tempText[i] = new THREE.Mesh(tempTextGeo, tempTextMat);

      const humTextGeo = new TextGeometry(humidiNum[i].toString() + '%', {
        font: font,
        size: 1.5,
        height: 0,
        curveSegments: 4,
        bevelEnabled: false,
        bevelThickness: 10,
        bevelSize: 1,
        bevelOffset: 0,
        bevelSegments: 1
      });
      humText[i] = new THREE.Mesh(humTextGeo, humTextMat);
      humText[i].name = 'humText' + i.toString()
      tempText[i].name = 'tempText' + i.toString()
      tempText[i].position.set(-8, i * height / 10, 0)
      humText[i].position.set(width + 2, i * height / 10, 0)
      diagram.add(humText[i]);
      diagram.add(tempText[i]);
    }
  });
}

// draw the data in diagram
function drawData() {
  try {
    let e = diagram.remove(diagram.getObjectByName('timeText1'));
    e = diagram.remove(diagram.getObjectByName('timeText2'));
    e = diagram.remove(diagram.getObjectByName('timeText3'));

  } catch (e) {

  }

  diagram.remove(weatherLine);
  diagram.remove(weatherHumLine);
  for (let j = 0; j < dataLine.length; j++) {
    diagram.remove(dataLine[j]);
    diagram.remove(dataHumLine[j]);
  }

  dataPoints = [[], [], [], [], [], [], [], [], [], []];
  dataHumPoints = [[], [], [], [], [], [], [], [], [], []];
  weatherPoints = [];
  weatherHumPoints = [];
  // create points vector for weather
  for (let i = dataStart; i < shownData; i++) {
    if (outData.length > 0) {
      try {
        if (outData[i].fields.timestamp < maxTimeStamp && outData[i].fields.timestamp > minTimeStamp) {
          const xvalue = (outData[i].fields.timestamp - minTimeStamp) / (maxTimeStamp - minTimeStamp) * width
          weatherPoints.push(new THREE.Vector3(xvalue, (outData[i].fields.temp) * height / 30, 0));
          weatherHumPoints.push(new THREE.Vector3(xvalue, (outData[i].fields.humidity) * height / 100, 0));
          let e = 0;
        }
      } catch (e) {

      }
    }
    // create points vector for sensor data
    for (let j = 0; j < localData.length; j++) {
      if (localData[j].length > 0) {
        try {
          if (localData[j][i].timestamp < maxTimeStamp && localData[j][i].timestamp > minTimeStamp) {
            const xvalue = (localData[j][i].timestamp - minTimeStamp) / (maxTimeStamp - minTimeStamp) * width
            dataPoints[j].push(new THREE.Vector3(xvalue, (localData[j][i].temp_in_deg) * height / 30, 0));
            dataHumPoints[j].push(new THREE.Vector3(xvalue, (localData[j][i].humid_perc) * height / 100, 0));
            let e = 0;
          }
        } catch (e) {

        }

      }
    }
  }
  // draw the lines
  const weatherGeo = new THREE.BufferGeometry().setFromPoints(weatherPoints);
  const weatherHumGeo = new THREE.BufferGeometry().setFromPoints(weatherHumPoints);
  weatherLine = new THREE.Line(weatherGeo, weatherMat);
  weatherHumLine = new THREE.Line(weatherHumGeo, weatherHumMat);
  diagram.add(weatherLine);
  diagram.add(weatherHumLine);

  for (let j = 0; j < dataPoints.length; j++) {
    if (dataPoints[j].length > 0) {
      const data1Mat = new THREE.LineBasicMaterial({ color: lineColor[j] });
      const data1HumMat = new THREE.LineBasicMaterial({ color: humColor[j] });
      const dataGeo = new THREE.BufferGeometry().setFromPoints(dataPoints[j]);
      const dataHumGeo = new THREE.BufferGeometry().setFromPoints(dataHumPoints[j]);
      dataLine[j] = new THREE.Line(dataGeo, data1Mat);
      dataHumLine[j] = new THREE.Line(dataHumGeo, data1HumMat);
      diagram.add(dataHumLine[j]);
      diagram.add(dataLine[j]);
    }
  }
  createDateText();
}

// draw the axis
function drawStatic() {
  diagram.remove(scaleYLine);
  diagram.remove(scaleY2Line);
  diagram.remove(scaleXLine);
  diagram.position.set(-width / 2, -height / 2, 0);

  scalePointsY2 = [];
  scalePointsY = [];
  scalePointsX = [];

  // create x axis
  scalePointsX.push(new THREE.Vector3(0, 0, 0));
  scalePointsX.push(new THREE.Vector3(0, -start, 0));
  scalePointsX.push(new THREE.Vector3(0, 0, 0));

  scalePointsX.push(new THREE.Vector3(width / 2, 0, 0));
  scalePointsX.push(new THREE.Vector3(width / 2, -start, 0));
  scalePointsX.push(new THREE.Vector3(width / 2, 0, 0));

  scalePointsX.push(new THREE.Vector3(width, 0, 0));
  scalePointsX.push(new THREE.Vector3(width, -start, 0));
  scalePointsX.push(new THREE.Vector3(width, 0, 0));

  const scaleXGeo = new THREE.BufferGeometry().setFromPoints(scalePointsX);
  scaleXLine = new THREE.Line(scaleXGeo, material);
  diagram.add(scaleXLine);
  // create y axis
  for (let i = 0; i < 11; i++) {
    scalePointsY.push(new THREE.Vector3(0, i * height / 10, 0));
    scalePointsY.push(new THREE.Vector3(-start, i * height / 10, 0));
    scalePointsY.push(new THREE.Vector3(0, i * height / 10, 0));

    scalePointsY2.push(new THREE.Vector3(width, i * height / 10, 0));
    scalePointsY2.push(new THREE.Vector3(width + start, i * height / 10, 0));
    scalePointsY2.push(new THREE.Vector3(width, i * height / 10, 0));
    // move the text
    try {

      let e = diagram.getObjectByName('tempText' + i.toString()).position.set(-8, i * height / 10, 0)
      e = diagram.getObjectByName('humText' + i.toString()).position.set(width + 2, i * height / 10, 0)
    } catch (e) {

    }

  }
  // draw the lines
  const scaleYGeo = new THREE.BufferGeometry().setFromPoints(scalePointsY);
  scaleYLine = new THREE.Line(scaleYGeo, material);
  diagram.add(scaleYLine);
  const scaleY2Geo = new THREE.BufferGeometry().setFromPoints(scalePointsY2);
  scaleY2Line = new THREE.Line(scaleY2Geo, dashedMat);
  diagram.add(scaleY2Line);
}

// create date text
function createDateText() {

  const timeTextMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
  loader.load('static/moduleLibs/examples/fonts/droid/droid_sans_mono_regular.typeface.json', function (font) {

    const time1TextGeo = new TextGeometry(new Date(minTimeStamp * 1000).toLocaleString('de-DE', { timezone: 'UTC+2' }), {
      font: font,
      size: 1.5,
      height: 0,
      curveSegments: 4,
      bevelEnabled: false,
      bevelThickness: 10,
      bevelSize: 1,
      bevelOffset: 0,
      bevelSegments: 1
    });
    const timeText1 = new THREE.Mesh(time1TextGeo, timeTextMat);
    timeText1.position.set(-8, -3, 0)
    timeText1.name = "timeText1";
    diagram.add(timeText1);

    const time2TextGeo = new TextGeometry(new Date((((maxTimeStamp - minTimeStamp) / 2) + minTimeStamp) * 1000).toLocaleString('de-DE', { timezone: 'UTC+2' }), {
      font: font,
      size: 1.5,
      height: 0,
      curveSegments: 4,
      bevelEnabled: false,
      bevelThickness: 10,
      bevelSize: 1,
      bevelOffset: 0,
      bevelSegments: 1
    });
    const timeText2 = new THREE.Mesh(time2TextGeo, timeTextMat);
    timeText2.position.set((width / 2) - 12, -3, 0)
    timeText2.name = "timeText2";
    diagram.add(timeText2);

    const time3TextGeo = new TextGeometry(new Date(maxTimeStamp * 1000).toLocaleString('de-DE', { timezone: 'UTC+2' }), {
      font: font,
      size: 1.5,
      height: 0,
      curveSegments: 4,
      bevelEnabled: false,
      bevelThickness: 10,
      bevelSize: 1,
      bevelOffset: 0,
      bevelSegments: 1
    });
    const timeText3 = new THREE.Mesh(time3TextGeo, timeTextMat);
    timeText3.position.set(width - 12, -3, 0)
    timeText3.name = "timeText3";
    diagram.add(timeText3);

  });
}
// create the legend text
function drawLegend() {
  loader.load('static/moduleLibs/examples/fonts/droid/droid_sans_mono_regular.typeface.json', function (font) {
    if (outData.length > 0) {
      const weatherTextGeo = new TextGeometry('Wetter', {
        font: font,
        size: 1.5,
        height: 0,
        curveSegments: 4,
        bevelEnabled: false,
        bevelThickness: 10,
        bevelSize: 1,
        bevelOffset: 0,
        bevelSegments: 1
      });
      const weatherText = new THREE.Mesh(weatherTextGeo, weatherMat);
      weatherText.position.set(width / 2, height, 0)
      diagram.add(weatherText);

    }

    for (let i = 0; i < localData.length; i++) {
      if (localData[i].length > 0) {
        const dataTextGeo = new TextGeometry(sensorData[i].fields.name, {
          font: font,
          size: 1.5,
          height: 0,
          curveSegments: 4,
          bevelEnabled: false,
          bevelThickness: 10,
          bevelSize: 1,
          bevelOffset: 0,
          bevelSegments: 1
        });
        const dataText = new THREE.Mesh(dataTextGeo, new THREE.LineBasicMaterial({ color: lineColor[i] }));
        dataText.position.set(width / 2, height - (height * (i + 1) / 30), 0)
        diagram.add(dataText);

      }
    }
  });


}
