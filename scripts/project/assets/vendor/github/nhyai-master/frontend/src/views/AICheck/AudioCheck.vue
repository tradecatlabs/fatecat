<template>
	<div class="audioCheck">
		<!--音频评审-->
		<div class="clearfix">
			<div class="show_voice_outer fl">
				<div class="outer_voice">
					<p class="voice_title">语音审查</p>
					<div class="voice_player_outer clearfix">
						<img src="../../assets/image/voice_mark.png" class="fl icon_music" id="music_icon">
						<div class="audio_wrapper_outer">
							<div class="audio-wrapper">
								<audio id="audio">
									<source :src="recordSrc" type="audio/wav">
								</audio>
								<div class="audio-left">
									<img id="audioPlayer" src="../../assets/image/audio/play.png">
								</div>
								<div class="audio-right">
									<div class="progress-bar-bg" id="progressBarBg">
										<span id="progressDot"></span>
										<div class="progress-bar" id="progressBar"></div>
									</div>
									<div class="audio-time">
										<span class="audio-length-current" id="audioCurTime">00:00</span>
										<span class="audio-length-total"></span>
									</div>
									<p style="max-width: 536px;">{{audioName}}</p>
								</div>
							</div>
						</div>

					</div>
					<div class="voice_result_outer">
						<div class="show_voice_word">
							<!--<span class="fl"> 1:05 - 1:06</span>-->
							<!--<span class="fl ell"> 好，现在<span class="red_color">违禁词</span>到室当中呢，<span class="red_color">违禁词</span>了三十位</span>-->
						</div>
					</div>
				</div>
				<p class="suggest"><span class="red_color">*</span> 提示: 敏感系数<50%为合规，50%～80%为疑似违规，>80%为违规<span v-show="imageIsBig" style="color: red;margin-left: 10px;display: inline-block;">！该图片大小超过1M</span></p>
			</div>
			<div class="show_json_outer fl">
				<p class="result_title">审查结果</p>
				<div>
					<div class="result_outer">
						<p>色情文字检测</p>
						<p class="green_style_name" v-if="isUploading">识别中...</p>
						<p class="red_style_name" v-else-if="isSex">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
					<div class="result_outer">
						<p>涉政文字检测 </p>
						<p class="green_style_name" v-if="isUploading">识别中...</p>
						<p class="red_style_name" v-else-if="isPolitics">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
					<div class="result_outer">
						<p>违禁品检测</p>
						<p class="green_style_name" v-if="isUploading">识别中...</p>
						<p class="red_style_name" v-else-if="isForce">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
					<div class="result_outer">
						<p>民谣类检测</p>
						<p class="green_style_name" v-if="isUploading">识别中...</p>
						<p class="red_style_name" v-else-if="isSong">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
				</div>
			</div>
		</div>

	</div>
</template>

<script>
    export default {
	    props:['stopAudio'],
	    data(){
            return{
                imageIsBig:false,
				recordSrc:"",
				resultType:[],
                audioName:'',
				isNone:true,
                isUploading:false,
                isSex:false,
                isForce:false,
                isSong:false,
                isPolitics:false

			}
        },
		mounted(){
            this.initAudioEvent();
		},
		watch:{
            stopAudio:(newVal)=>{
                if(newVal){
                    const audio = document.getElementsByTagName('audio')[0];
                    const audioPlayer = document.getElementById('audioPlayer');
                    const musicIcon = document.getElementById('music_icon');
                    console.log(newVal);
                    audio.pause();
                    audioPlayer.src =require( '../../assets/image/audio/play.png');
                    musicIcon.src =require( '../../assets/image/voice_mark.png');
				}
			}
		},
		methods:{
            initAudioEvent(){
                var audio = document.getElementsByTagName('audio')[0];
                var audioPlayer = document.getElementById('audioPlayer');
                var musicIcon = document.getElementById('music_icon');
                // 监听音频播放时间并更新进度条
                audio.addEventListener('timeupdate', ()=>{
                    this.updateProgress(audio);
                }, false);

                // 监听播放完成事件
                audio.addEventListener('ended', ()=> {
                    this.audioEnded();
                }, false);

                // 点击播放/暂停图片时，控制音乐的播放与暂停
                audioPlayer.addEventListener('click', ()=> {
                    // 改变播放/暂停图片
                    if (audio.paused) {
                        // 开始播放当前点击的音频
                        audio.play();
                        audioPlayer.src =require('../../assets/image/audio/pause.png') ;
                        musicIcon.src = require('../../assets/image/audio/icon-music.gif');
                    } else {
                        audio.pause();
                        audioPlayer.src =require( '../../assets/image/audio/play.png');
                        musicIcon.src = require('../../assets/image/voice_mark.png');
                    }
                }, false);

                // 点击进度条跳到指定点播放
                // PS：此处不要用click，否则下面的拖动进度点事件有可能在此处触发，此时e.offsetX的值非常小，会导致进度条弹回开始处（简直不能忍！！）
                var progressBarBg = document.getElementById('progressBarBg');
                progressBarBg.addEventListener('mousedown', (event)=> {
                    // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
                    if (!audio.paused || audio.currentTime != 0) {
                        var pgsWidth = parseFloat(window.getComputedStyle(progressBarBg, null).width.replace('px', ''));
                        var rate = event.offsetX / pgsWidth;
                        audio.currentTime = audio.duration * rate;
                        this.updateProgress(audio);
                    }
                }, false);

                // 拖动进度点调节进度
                this.dragProgressDotEvent(audio);
            },

            /**
             * 鼠标拖动进度点时可以调节进度
             * @param {*} audio
             */
            dragProgressDotEvent(audio) {
                var dot = document.getElementById('progressDot');

                var position = {
                    oriOffestLeft: 0, // 移动开始时进度条的点距离进度条的偏移值
                    oriX: 0, // 移动开始时的x坐标
                    maxLeft: 0, // 向左最大可拖动距离
                    maxRight: 0 // 向右最大可拖动距离
                };
                var flag = false; // 标记是否拖动开始

                // 鼠标按下时
                dot.addEventListener('mousedown', down, false);
                dot.addEventListener('touchstart', down, false);

                // 开始拖动
                document.addEventListener('mousemove', move, false);
                document.addEventListener('touchmove', move, false);

                // 拖动结束
                document.addEventListener('mouseup', end, false);
                document.addEventListener('touchend', end, false);

                function down(event) {
                    if (!audio.paused || audio.currentTime != 0) { // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
                        flag = true;

                        position.oriOffestLeft = dot.offsetLeft;
                        position.oriX = event.touches ? event.touches[0].clientX : event.clientX; // 要同时适配mousedown和touchstart事件
                        position.maxLeft = position.oriOffestLeft; // 向左最大可拖动距离
                        position.maxRight = document.getElementById('progressBarBg').offsetWidth - position.oriOffestLeft; // 向右最大可拖动距离

                        // 禁止默认事件（避免鼠标拖拽进度点的时候选中文字）
                        if (event && event.preventDefault) {
                            event.preventDefault();
                        } else {
                            event.returnValue = false;
                        }

                        // 禁止事件冒泡
                        if (event && event.stopPropagation) {
                            event.stopPropagation();
                        } else {
                            window.event.cancelBubble = true;
                        }
                    }
                }

                function move(event) {
                    if (flag) {
                        var clientX = event.touches ? event.touches[0].clientX : event.clientX; // 要同时适配mousemove和touchmove事件
                        var length = clientX - position.oriX;
                        if (length > position.maxRight) {
                            length = position.maxRight;
                        } else if (length < -position.maxLeft) {
                            length = -position.maxLeft;
                        }
                        var progressBarBg = document.getElementById('progressBarBg');
                        var pgsWidth = parseFloat(window.getComputedStyle(progressBarBg, null).width.replace('px', ''));
                        var rate = (position.oriOffestLeft + length) / pgsWidth;
                        audio.currentTime = audio.duration * rate;
                        this.updateProgress(audio);
                    }
                }

                function end() {
                    flag = false;
                }
            },

			/**
			 * 停止播放
			 * */
			pauseAudio(){
                var audio = document.getElementsByTagName('audio')[0];
                var audioPlayer = document.getElementById('audioPlayer');
                var musicIcon = document.getElementById('music_icon');
                audio.stop();
                audioPlayer.src =require( '../../assets/image/audio/play.png');
                musicIcon.src =require( '../../assets/image/voice_mark.png');
			},

            /**
             * 更新进度条与当前播放时间
             * @param {object} audio - audio对象
             */
            updateProgress(audio) {
                var value = audio.currentTime / audio.duration;
                document.getElementById('progressBar').style.width = value * 100 + '%';
                document.getElementById('progressDot').style.left = value * 100 + '%';
                document.getElementById('audioCurTime').innerText = this.transTime(audio.currentTime);
                document.getElementsByClassName('audio-length-total')[0].innerText = this.transTime(audio.duration);
            },

            /**
             * 播放完成时把进度调回开始的位置
             */
            audioEnded() {
                document.getElementById('progressBar').style.width = 0;
                document.getElementById('progressDot').style.left = 0;
                document.getElementById('audioCurTime').innerText = this.transTime(0);
                document.getElementById('audioPlayer').src =require( '../../assets/image/audio/play.png');
                document.getElementById('music_icon').src =require( '../../assets/image/voice_mark.png');
            },

            /**
             * 音频播放时间换算
             * @param {number} value - 音频当前播放时间，单位秒
             */
            transTime(value) {
                var time = "";
                var h = parseInt(value / 3600);
                value %= 3600;
                var m = parseInt(value / 60);
                var s = parseInt(value % 60);
                if (h > 0) {
                    time = this.formatTime(h + ":" + m + ":" + s);
                } else {
                    time = this.formatTime(m + ":" + s);
                }

                return time;
            },

            /**
             * 格式化时间显示，补零对齐
             * eg：2:4  -->  02:04
             * @param {string} value - 形如 h:m:s 的字符串
             */
            formatTime(value) {
                var time = "";
                var s = value.split(':');
                var i = 0;
                for (; i < s.length - 1; i++) {
                    time += s[i].length == 1 ? ("0" + s[i]) : s[i];
                    time += ":";
                }
                time += s[i].length == 1 ? ("0" + s[i]) : s[i];

                return time;
            },
            submitAudio(e,file){
                this.isUploading = true;
                this.isSex = false;
                this.isPolitics = false;
                this.isSong = false;
                this.isForce = false;
                this.recordSrc = URL.createObjectURL(file);
                document.getElementsByClassName('show_voice_word')[0].innerHTML='';
                console.log(file);
                this.audioName = file.name;
                var loading = this.$loading({fullscreen:false,target:document.querySelector(".outer_voice")});
                console.log("音频提交中。。。")
                var formData = new FormData();
                formData.append('speech', file);
                $.ajax({
                    url: this.api+"/api/v1/audio/get_chinese_speech_inspection/",
                    type: "post",
                    timeout : 600000,
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        console.log(response);
                        this.isUploading = false;
                        var audio = document.getElementById('audio').load();
                        window.setTimeout(()=>{
                            var audio = document.getElementById('audio');
							document.getElementsByClassName('audio-length-total')[0].innerText = this.transTime(audio.duration);
							document.getElementsByClassName('show_voice_word')[0].innerHTML= response.data.speech_contents.web_text;
                            loading.close();
						},100);
//                        this.updateProgress(audio);
                        if(response.data.speech_contents.final_list.length!=0){
                            response.data.speech_contents.final_list.forEach(item=>{
                                if(item.indexOf('色情')!=-1){
                                    this.isSex = true;
                                }else if(item.indexOf('政治')!=-1){
                                    this.isPolitics = true;
                                }else if(item.indexOf('民谣')!=-1){
                                    this.isSong = true;
                                }else if(item.indexOf('违禁品')!=-1){
                                    this.isForce = true;
                                }
                            });
                        }
                        this.$parent.changeUploadState(false);
                    },
                    error:err=>{
                        loading.close();
                        console.log(err);
                        this.$parent.changeUploadState(false);
                        this.$message.error('上传失败,重新上传！');
                    }
                });
                e.preventDefault();
            }
		}
	}
</script>

<style scoped>
	@import "../../assets/css/audio.css";
	/*音频样式begin*/
	.audioCheck{width: 1200px;margin: 0 auto;}
	.show_voice_outer{min-height: 440px;width: 800px;}
	.outer_voice{height:500px;z-index: 1;text-align: center;background-color: #f4f5f7;padding-right: 20px;}
	.voice_title{height: 34px;line-height:34px;width: 135px;margin: 0 auto;background-color: #deecf9;color: #007bff;margin-bottom: 20px;}
	.voice_player_outer{height: 125px;width: 94%;margin: 10px auto;border-radius: 5px;background-color: white;}
	.voice_result_outer{height: 290px;background-color: white;width: 94%;margin: 10px auto;border-radius: 5px;overflow-y: auto;overflow-x: hidden;}
	.audio_wrapper_outer{margin-left: 180px;margin-right: 20%;}
	.icon_music{margin: 25px 0 0 95px;}
	.show_voice_word{margin: 20px ;color: #010101;font-size: 14px;display: flex}
	.show_voice_word span{display: inline-block;text-align: left;}
	.show_voice_word span:nth-of-type(2){margin-left: 20px;flex: 1;}

	.show_json_outer{width:400px;height: 430px;z-index: 99;background-color: white;position: relative;left: -20px;top: 35px;box-shadow:5px 0 20px #c5cff1;overflow-y: auto;}
	.show_json_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.show_json_outer .result_title:before{content: "";background: url("../../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.suggest{color: #b2b2b2;font-size: 14px;min-height: 30px;margin:8px 0;}
	.result_outer{margin: 20px auto;display: flex;color: #000000;height: 28px;line-height: 28px;width: 240px;}
	.result_outer p:nth-of-type(1){font-size: 16px;width: 120px;}
	.result_outer p:nth-of-type(2){font-size: 16px;width: 120px;text-align: center}
	.result_outer p:nth-of-type(3){font-size: 16px;flex: 4;text-align: center}
	.result_outer .green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff;text-align: center;}
	.result_outer .green_style_number{border: 1px solid #54cd62;color: #54cd62}
	.result_outer .orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.result_outer .orange_style_number{border: 1px solid #ffac09;color: #ffac09}
	.result_outer .red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}
	.result_outer .red_style_number{border: 1px solid #ff524a;color: #ff524a}
	.orange_color{color: #ffac09;}
	.red_color{color: #ff524a;}
</style>