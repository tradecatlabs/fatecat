<template>
	<div id="yellow">
		<Navigation></Navigation>
		<div class="yellow_top_contain">
			<el-row>
				<el-row>
					<el-col :xl={span:24}>
						<div class="banner_outer ai-common-banner">
							<!--<img src="../assets/image/yellow/yellow_banner.png" alt="">-->
							<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
								<div class="describe_outer_banner ">
									<p class="ell">色情检测</p>
									<p class="ell-rows-4 ">基于海量大数据样本，领先机器学习算法，高效识别涉黄图<br/>片，精准鉴别图像中的涉黄内容，规避运营风险</p>
									<p class="practice_online" @click="toPractice">在线体验</p>
								</div>
							</el-col>
						</div>
					</el-col>
				</el-row>
			</el-row>
		</div>
		<div class="functional_experience" >
			<h2 class="title">功能介绍</h2>
			<p class="title_describe">人工智能鉴黄技术，智能识别图片和色情和性感内容，让您的应用轻松过审，远离违规风险</p>
			<div class="handwrite">
				<el-row>
					<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
						<div class="top_nav_image_outer clearfix">
							<div class="sample_item fl" v-for="(item,index) in sampleList">
								<img :src="item.src" alt="">
								<div class="sample_result_outer">
									<p class="red_style_name" v-if="item.number>90">违规</p>
									<p class="orange_style_name" v-else-if="item.number>50">疑似违规</p>
									<p class="green_style_name" v-else>合规</p>
									<p class="red_style_number" v-if="item.number>90">{{item.number}}%</p>
									<p class="orange_style_number" v-else-if="item.number>50">{{item.number}}%</p>
									<p class="green_style_number" v-else>{{item.number}}%</p>
								</div>
							</div>
							<!--<img src="../assets/image/force/force_sample.png" alt="">-->
						</div>
					</el-col>
				</el-row>
			</div>
		</div>
		<div class="functional_experience" id="practice_title">
			<h2 class="title">功能体验</h2>
			<div class="suggest_outer">
				<div  class="current_width_style_1040 clearfix">
					<div class="show_input_outer fl">
						<input type="file" id="url_input" class="inputfile" readonly placeholder="请选择本地图片" accept="image/*" @change="changeImage($event)" multiple>
						<label for="url_input" class="init_url_style">请选择本地图片上传</label>
						<!--<p class="check_style">检测</p>-->
						<!--<p class="check_style_hidden" @click="urlCheck">检测</p>-->
					</div>
					<div class="local_upload fl" v-if="!isCheck">
						<!--<p>本地上传</p>-->
						<input id="datafile" name="datafile" type="file" accept="image/*" class="inputfile" @change="changeImage($event)" multiple>
						<label for="datafile">本地上传</label>
					</div>
					<div class="local_upload fl" v-else>
						<p class="is_check">正在检测</p>
					</div>
				</div>
				<p class="top_suggest current_width_style_1040">图片文件类型支持PNG、JPG、JPEG，图片大小不超过20M。</p>
			</div>

			<div class="choose_image current_width_style" v-show="isImage==1">
				<div class="add_before ">
					<!--<img src="../assets/image/yellow/image_upload.png" alt="">-->
					<el-upload
						class="avatar-uploader"
						action="http://172.31.4.7:8000/api/v1/image/get_vision_porn/"
						:auto-upload="false"
						:multiple="true"
						:limit="limit"
						:show-file-list="false"
						accept="image/png,image/jpg,image/jpeg"
						:on-exceed="outSuggest"
						:on-change="onImageChange">
						<i class="el-icon-plus avatar-uploader-icon"></i>
					</el-upload>
				</div>
				<p class="choose_suggest">支持图片多张上传，一次检测十张</p>
			</div>
			<div class="choose_image_list current_width_style" v-show="isImage==2" >
				<el-upload
					ref="upload"
					:class="{hide:hideUpload}"
					action="http://172.31.4.7:8000/api/v1/image/get_vision_porn/"
					list-type="picture-card"
					:auto-upload="false"
					:on-preview="handlePictureCardPreview"
					:file-list="fileList"
					:multiple="true"
					:limit="limit"
					:on-change="onListChange"
					:http-request="uploadImage"
					:on-exceed="outSuggest"
					accept="image/png,image/jpg,image/jpeg"
					:on-remove="handleRemove">
					<i class="el-icon-plus"></i>
				</el-upload>
				<el-dialog :visible.sync="dialogVisible">
					<img width="100%" :src="dialogImageUrl" alt="">
				</el-dialog>
				<p class="begin_check" @click="submitUpload($event)">开始检测</p>
			</div>
			<div class="choose_result current_width_style" v-show="isImage==3">
				<div class="result_title">
					<img src="../assets/image/yellow/yellow_result_top.png" alt="">
					<span>色情识别  |  审查结果</span>
					<div class="yellow_result_outer clearfix" >
						<div class="fl" v-for="item in resultList">
							<img :src="item.image" alt="">
							<div class="result_outer" v-if="item.number>80">
								<p class="red_style_name">违规</p>
								<p class="red_style_number">{{item.number}}%</p>
							</div>
							<div class="result_outer" v-else-if="item.number>50">
								<p class="orange_style_name">疑似违规</p>
								<p class="orange_style_number">{{item.number}}%</p>
							</div>
							<div class="result_outer" v-else>
								<p class="green_style_name">合规</p>
								<p class="green_style_number">{{item.number}}%</p>
							</div>
						</div>
					</div>
				</div>
				<p class="again_check" @click="uploadAgain">换一批检测</p>
				<p class="yellow_result_suggest"><span class="">*</span>提示：检测结果百分比越高代表违规越严重</p>
			</div>
		</div>
		<div class="recommended_scenario">
			<h2 class="title">应用场景</h2>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<div style="width: 70%;margin: 0 auto;">
						<el-carousel  type="card" height="250px"  trigger="click"><!--:interval="4000"-->
							<el-carousel-item v-for="(item,index) in recommendedList" :key="index">
								<img :src="item.imgUrl" alt="">
								<h3 class="medium">{{ item.imgUrl }}</h3>
							</el-carousel-item>
						</el-carousel>
					</div>
				</el-col>
			</el-row>
		</div>
		<div class="advantage_product" >
			<h2 class="title">技术优势</h2>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<el-row align="left">
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image title_image_common"></i>
							<div class="show_advantage_describe">
								<span>准确率高</span>
								<div class="describe_outer">
									<p class="good_describe">目前准确率可达90%以上，基于智能的深度学习算法，准确度还将不断提高。</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_two title_image_common"></i>
							<div class="show_advantage_describe">
								<span>及时高效</span>
								<div class="describe_outer">
									<p class="good_describe">能够对用户上传的图片自动审核，主动发现潜在的暴恐图片，打击精度高，覆盖广，响应快。</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_three title_image_common"></i>
							<div class="show_advantage_describe">
								<span>灵活性定制</span>
								<div class="describe_outer">
									<p class="good_describe">根据用户审核平台需求，深度定制产品策略与解决方案。</p>
								</div>
							</div>
						</el-col>
					</el-row>
				</el-col>
			</el-row>
		</div>
		<FooterIndex></FooterIndex>
	</div>

</template>

<script>
    import fileUtil from '../store/fileUtil'
    import {scrollBy} from '../store/common'
	import Navigation from "../components/navigation.vue"
    import FooterIndex from "../components/footerIndex.vue"
    export default {
        data() {
			return{
                dialogImageUrl: "",
                dialogVisible: false,
                jsonDemo:'{"ret":0,"msg":"ok","data":{"tag_list":[{"tag_name":"protest","probability":0.3087675468623638},{"tag_name":"violence","probability":0.017580988407135},{"tag_name":"sign","probability":0.795149803161621},{"tag_name":"photo","probability":0.0147841582074761},{"tag_name":"fire","probability":0.0184208210557699},{"tag_name":"police","probability":0.0153429144993424},{"tag_name":"children","probability":0.00931504089385271},{"tag_name":"group_20","probability":0.683478415012359},{"tag_name":"group_100","probability":0.207240253686904},{"tag_name":"flag","probability":0.122076518833637},{"tag_name":"night","probability":0.212110564112663},{"tag_name":"shouting","probability":0.0291868895292282}]}}',
                buttonWord:"开始检测",
                imageName:"",
                showPercent:"概率：1.75%",
                isForce:false,
                imageRight:false,
                imageIsBig:false,
                activeName: 'first',
                showJson :{},
                options:{background:"rgba(0, 0, 0, 0.3)",fullscreen:false,target:document.querySelector(".show_json_outer")},
                currentImage:1,
                isLoading:false,
                clickFirst:0,
                fileList: [],
				isImage:1,
                imgUrl1:require('../../static/imgs/usage_image1.png'),
                imgUrl2:require('../../static/imgs/usage_image2.png'),
                imgUrl3:require('../../static/imgs/usage_image03.png'),
                recommendedList:[{'imgUrl':"../../static/imgs/usage_image1.png"},{'imgUrl':'../../static/imgs/usage_image2.png'},{'imgUrl':'../../static/imgs/usage_image03.png'}],
                srcList:[],
                url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
				completeNumber:0,
				resultList:[],
                sampleList:[{src:require("../assets/image/yellow/sample_image1.png"),number:79.90},{src:require("../assets/image/yellow/sample_image2.png"),number:11.42},{src:require("../assets/image/yellow/sample_image3.png"),number: 29.83},
                    {src:require("../assets/image/yellow/sample_image4.png"),number:1.63},{src:require("../assets/image/yellow/sample_image5.png"),number:20.61},{src:require("../assets/image/yellow/sample_image6.png"),number:0.04}],
                isCheck:false,
                hideUpload:false,
				limit:10
			}
        },
        mounted:function () {
        },
        methods: {
            urlCheck(){
                this.$message.error('该功能尚未开通！')
			},
            onImageChange(file, fileList){
                console.log(file,"走了这里");
                fileUtil.getOrientation(file.raw).then((orient) => {
                    if(orient && orient === 6) {
                        const reader = new FileReader();
                        reader.onload = ($event)=> {
                            let img = new Image();
                            img.src = $event.target.result;
                            img.onload = ()=> {
                                const data = fileUtil.rotateImage(img, img.width, img.height);
                                const newFile = fileUtil.dataURLtoFile(data, file.raw.name);
                                console.log(newFile);
                                file.url= fileUtil.getObjectURL(newFile);
                                file.raw = newFile;
                                if(this.fileList.length<this.limit){
                                    if(file.size>20971520){
                                        this.$message.error('图片'+file.name+'大于20M,请选择小于20M的图片！');
                                    }else {
                                        this.fileList.push(file);
                                        this.isImage = 2;
                                    }
                                }
                            }
                        };
                        reader.readAsDataURL(file.raw);

                    } else {
                        if(!file.url){
                            file.url = URL.createObjectURL(file.raw);
                        }
                        if(this.fileList.length<this.limit){
                            if(file.size>20971520){
                                this.$message.error('图片'+file.name+'大于20M,请选择小于20M的图片！');
                            }else {
                                this.fileList.push(file);
                                this.isImage = 2;
                            }
                        }
                    }
                });
                if(fileList.length===this.limit){
                    this.$message.error('一次最多选择10张图片！');
                    this.hideUpload = true;
                }
//                this.fileList.push(file);

            },
            onListChange(file, fileList){
                this.checkDegree(file,fileList);
                if(fileList.length===this.limit){
                    this.$message.error('一次最多选择10张图片！');
                    this.hideUpload = true;
                }
            },
            outSuggest(files, fileList){
                console.log(files);
                let x = 0;
                let that = this;
                console.log(x);
                while(x<files.length&&this.fileList.length<this.limit){
                    let file = files[x];
                    var newFile = {};
                    newFile.name = file.name;
                    newFile.uid = file.uid;
                    newFile.size = file.size;
                    newFile.status = "ready";
                    newFile.url = URL.createObjectURL(file);
                    newFile.raw = file;
//                    this.fileList.push(newFile);
                    if(file.size>20971520){
                        this.$message.error('图片'+newFile.name+'大于20M,请选择小于20M的图片！');
                    }else {
                        that.fileList.push(newFile);
                    }
                    x++;
                }
                this.isImage = 2;
                this.hideUpload =true;
                this.$message.error('一次最多选择10张图片！');
			},
            checkDegree(file,fileList) {
                fileUtil.getOrientation(file.raw).then((orient) => {
                    if (orient && orient === 6) {
                        const reader = new FileReader();
                        reader.onload = ($event) => {
                            let img = new Image();
                            img.src = $event.target.result;
                            img.onload = () => {
                                const data = fileUtil.rotateImage(img, img.width, img.height);
                                const newFile = fileUtil.dataURLtoFile(data, file.raw.name);
                                console.log(newFile);
                                file.url = fileUtil.getObjectURL(newFile);
                                file.raw = newFile;
                                if (this.fileList.length < this.limit) {
                                    if(file.size>20971520){
                                        this.$message.error('图片'+file.name+'大于20M,请选择小于20M的图片！');
                                        fileList.splice(fileList.length-1,1)
                                    }else {
                                        this.fileList.push(file);
                                    }
                                }
                            }
                        };
                        reader.readAsDataURL(file.raw);
                    } else {
                        if (this.fileList.length < this.limit) {
//                            this.fileList.push(file);
                            if(file.size>20971520){
                                this.$message.error('图片'+file.name+'大于20M,请选择小于20M的图片！');
                                fileList.splice(fileList.length-1,1);
                            }else {
                                this.fileList.push(file);
                            }
                        }
                    }
                });
            },
            changeImage(e){
                var files = e.target.files;
                console.log(files);
                let j = 0;
                while(j<files.length&&this.fileList.length<this.limit){
                    let file = files[j];
                    var newFile = {};
                    newFile.name = file.name;
                    newFile.uid = file.uid;
                    newFile.size = file.size;
                    newFile.status = "ready";
                    newFile.url = URL.createObjectURL(file);
                    newFile.raw = file;
//                    this.fileList.push(newFile);
                    if(file.size>20971520){
                        this.$message.error('请选择小于20M的图片！');
                    }else {
                        this.fileList.push(newFile);
                    }
                    j++;
                }
                if(this.fileList.length>=10){
                    this.hideUpload = true;
                    this.$message.error('一次最多选择10张图片！');
                }
                if(this.fileList.length>0){
                    this.isImage = 2;
                }
            },
            submitUpload(e){
                if(this.fileList.length==0){
                    this.$message.error("请先选择图片！")
                    return;
                }
                this.isCheck= true;
                this.completeNumber= 0;
                this.resultList=[];
//                this.$refs.upload.submit();
				console.log(this.fileList);
                var loading = this.$loading({fullscreen:false,target:document.querySelector(".choose_image_list")});
                this.fileList.forEach(file=>{
                    this.uploadImageTotal(e,file.raw,loading);
				})
			},
            uploadImageTotal(e,file,loading){
                this.imageRight = false;
//                this.loading = this.$loading(this.options);
                this.isLoading= true;
                var formData = new FormData();
                formData.append('image', file);
                $.ajax({
                    url: this.api+"/api/v1/image/get_vision_porn/",
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        console.log(response);
                        this.completeNumber++;
                        this.resultList.push({
							image:response.image,
							number:response.data.normal_hot_porn
						});
                        if(this.completeNumber==this.fileList.length){
                            console.log("complete",this.fileList.length);
                            loading.close();
                            this.isImage = 3;
                            this.isCheck= false;
						}
                    },
                    error:(error)=>{
                        this.$message.error('上传失败，请重新上传！');
                        loading.close();
                    }
                });
                e.preventDefault();
            },
            uploadImage(e,file){
                this.isCheck= true;
                if(this.isImage == 1){
                    var loading = this.$loading({fullscreen:false,target:document.querySelector(".choose_image")});
                }else if(this.isImage == 2){
                    var loading = this.$loading({fullscreen:false,target:document.querySelector(".choose_image_list")});
                }else {
                    var loading = this.$loading({fullscreen:false,target:document.querySelector(".choose_result")});
                }
                var formData = new FormData();
                formData.append('image', file);
                $.ajax({
                    url: this.api+"/api/v1/image/get_vision_porn/",
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        this.resultList=[];
                        console.log(response);
                        this.resultList.push({
                            image:response.image,
                            number:response.data.normal_hot_porn
                        });
                        this.isImage = 3;
                        this.isCheck= false;
                        loading.close();
                    },
					error:(err)=>{

					}
                });
                e.preventDefault();
            },
            uploadAgain(){
                this.isImage = 1;
                this.fileList = [];
			},
            handleRemove(file, fileList) {
                console.log(file, fileList);
                this.fileList = fileList;
                console.log(this.fileList.length);
                window.setTimeout(()=>{
                    this.hideUpload = fileList>=this.limit;
				},500)


            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },
            toPractice(){
                scrollBy(document.getElementById('practice_title').offsetTop-100);
//                window.scrollBy(0,document.getElementById('practice_title').offsetTop-100)
            }
        },
		components:{
            Navigation,
            FooterIndex
		},

    }

</script>

<style scoped>
	.yellow_top_contain{font-size: 0;line-height: 0;text-align: center}
	.yellow_top_contain img{height: 480px;min-width: 1300px;}
	.yellow_top_contain .banner_outer{background-image: url('../assets/image/yellow/yellow_banner.png');min-width: 1300px;}
	.yellow_top_contain .describe_outer_banner{position: absolute;top:25%;font-size: 16px;color: white;width: 28%;height: 75%;}
	.yellow_top_contain .describe_outer_banner p{}
	.yellow_top_contain .describe_outer_banner p:nth-of-type(1){font-size: 30px;height: 60px;line-height: 60px;margin-bottom: 15px;min-width: 400px;text-align: left}
	.yellow_top_contain .describe_outer_banner p:nth-of-type(2){height: 105px;text-align: justify;overflow: hidden;min-width: 550px;line-height: 30px;}
	.yellow_top_contain  img{width: 100%;min-width: 1200px;}
	.yellow_top_contain .practice_online{height: 40px;line-height:40px;width: 135px;font-size: 15px;text-align: center;color: #fff;border: 1px solid #fff;cursor:pointer}
	.yellow_top_contain .practice_online:hover{background-color: white;color: #000;}

	.functional_experience{margin: 50px 0;}
	.functional_experience .title{text-align: center;color: #000;margin: 40px 0 15px;font-size: 30px;}
	.functional_experience .title_describe{text-align: center;color: #000;font-size: 14px;margin-bottom: 50px;}

	.top_nav_image_outer{text-align: center;width: 860px;margin: 15px auto;}
	.top_nav_image_outer a img{width: 100%;}
	.top_nav_image_outer .sample_item{width: 260px;margin-bottom: 35px;margin-right: 40px;}
	.top_nav_image_outer .sample_item:nth-of-type(3n){margin-right: 0}
	.top_nav_image_outer .sample_item img{width: 260px;height: 200px;}
	.sample_result_outer{margin: -20px auto 0;display: flex;color: #000000;height: 28px;line-height: 28px;width: 60%;}
	.sample_result_outer p:nth-of-type(1){font-size: 14px;flex: 5;}
	.sample_result_outer p:nth-of-type(2){font-size: 14px;flex: 4;text-align: center;background-color:white}
	.green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff}
	.green_style_number{border: 1px solid #54cd62;color: #54cd62}
	.orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.orange_style_number{border: 1px solid #ffac09;color: #ffac09}
	.red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}
	.red_style_number{border: 1px solid #ff524a;color: #ff524a}

	.suggest_outer{margin: 40px 0 20px;}
	.top_suggest{color: #999999;font-size: 14px;line-height: 40px;height: 30px;}
	.init_url_style{flex: 1;height: 35px;line-height: 35px;border: 1px solid #E2ECFC;font-size: 15px;padding-left: 10px;color: #666666;cursor: pointer;}
	/*.init_url_style:hover{border: 1px solid #C0C4CC;border-right: none;}*/
	/*.init_url_style:focus{border: 1px solid #409EFF;border-right: none;}*/
	.check_style{display:inline-block;height: 33px;line-height: 33px;font-size: 16px;color: #316DFF;border: 2px solid #316DFF;background-color: #FAFCFE;
		width: 100px;text-align: center;cursor:pointer;}
	.check_style_hidden{display:inline-block;height: 33px;line-height: 33px;font-size: 16px;color: #666666;border: 2px solid #f5f5f5;
		width: 100px;text-align: center;cursor:pointer;background-color: #f5f5f5}
	.check_style:hover{background-color: #316DFF;color: white;}
	.local_upload{height: 33px;line-height: 33px;font-size: 16px;}
	/*.local_upload:before{content: "或";margin: 0 25px;}*/
	.inputfile{z-index: -11111;width: 0px;height:1px;opacity: 0;position: absolute;}
	.is_check{display:inline-block;height: 35px;line-height: 35px;font-size: 16px;background-color: #f5f5f5;color:#666666;border: 1px solid #dddddd;padding: 0 15px;text-align: center;}
	.local_upload label{display:inline-block;height: 33px;line-height: 33px;font-size: 16px;background-color: #316DFF;color:white;border: 2px solid #316DFF;width: 100px;text-align: center;cursor: pointer;}
	.local_upload label:hover{background-color: #6087F7;color: white;border: 2px solid #6087F7;}
	.show_input_outer{display: flex;width: 800px;}
	.choose_image{border: 2px dashed #acc3ff;padding: 40px 0 40px 40px;position: relative;margin-top: 15px;height: 340px;overflow: hidden;}
	.choose_image_list{border: 2px dashed #acc3ff;padding: 40px 0 40px 40px;position: relative;margin-top: 15px;min-height: 330px;}
	.choose_result{border: 2px dashed #acc3ff;padding: 15px 0 30px 40px;position: relative;margin-top: 15px;min-height: 330px;}
	.add_before{width: 160px;height: 160px;margin: 50px auto 15px;}
	.choose_suggest{text-align: center;font-size: 14px;color: #333;}
	.begin_check{width: 160px;height: 45px;line-height: 45px;background-color: #316DFF;color: white;font-size: 16px;margin: 50px auto 0;text-align: center;cursor: pointer;}
	.again_check{width: 160px;height: 45px;line-height: 45px;border:1px solid #E2E5E8;background-color: #ffffff;color: #333333;font-size: 16px;margin: 40px auto 0;text-align: center;cursor: pointer;}
	.begin_check:hover{background-color: #6087F7;color: white;}
	.yellow_result_outer{margin-top: 15px;}
	.yellow_result_outer>div{width: 160px;overflow: hidden;text-align: center;margin-right: 40px;}
	.yellow_result_outer>div>img{width: 160px;height: 160px;object-fit: cover;}
	.result_title{text-align: center;vertical-align: middle;}
	.result_title img{vertical-align: middle;}
	.result_title span{vertical-align: middle;font-size: 18px;}
	.result_outer{margin: 10px 2px;display: flex;color: #000000;height: 28px;line-height: 28px;}
	.result_outer p:nth-of-type(1){font-size: 16px;flex: 5;}
	.result_outer p:nth-of-type(2){font-size: 16px;flex: 4;text-align: center}
	.result_outer .green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff}
	.result_outer .green_style_number{border: 1px solid #54cd62;color: #54cd62}
	.result_outer .orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.result_outer .orange_style_number{border: 1px solid #ffac09;color: #ffac09}
	.result_outer .red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}
	.result_outer .red_style_number{border: 1px solid #ff524a;color: #ff524a}
	.yellow_result_suggest{text-align: center;font-size: 15px;color: #999999;margin-top: 10px;}
	.yellow_result_suggest span{color: #ff4949;}
	.current_width_style{width: 1000px;margin: 0 auto;}
	.current_width_style_1040{width: 1040px;margin: 0 auto;}



	.advantage_product{padding: 65px 0 30px ;overflow: hidden;background-color: #f2f2f5;}
	.advantage_product .title{text-align: center;color: #000000;margin: 10px 0;font-size: 30px;}
	.advantage_product span{display: inline-block;padding: 10px;}
	.title_image_common{width: 70px; height: 70px;display: inline-block;margin-top: 50px;background-size: 70px 70px;}
	.title_image{background-image: url("../assets/image/yellow/yellow_advantage1.png");}
	.title_image_two{background-image: url("../assets/image/yellow/yellow_advantage2.png");}
	.title_image_three{background-image: url("../assets/image/yellow/yellow_advantage3.png");}
	.good_describe{font-size: 16px;color: #666666;line-height: 25px;text-align: center;}
	.describe_outer{width: 90%;margin: 0 auto;text-align: left}
	.show_advantage_describe{padding: 14px;}
	.show_advantage_describe span{font-size: 24px;color: #333333;}


	.recommended_scenario{padding: 50px 0 ;overflow: hidden;background-color: #fff;}
	.recommended_scenario .title{text-align: center;color: #000000;margin: 50px 0;font-size: 30px;}
	.recommended_scenario span{display: inline-block;padding: 10px;}
	.recommended_scenario img{width: 100%;height: 100%;}


</style>