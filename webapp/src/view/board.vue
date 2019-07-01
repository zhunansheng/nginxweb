/* eslint-disable */
<template>
  <div>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">
            磁盘数据清理
          </p>
          <div class="edittable-test-con">
            <div id="showImage" class="margin-bottom-10">
              <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="150">
                <Row>
                  <Col span="12">
                    <FormItem label="标题:">
                      <Input v-model="formItem.title" type="textarea" :autosize="true" placeholder=""></Input>
                    </FormItem>
                  </Col>
                </Row>
               <Row>
                  <Col span="24">
                  <FormItem label="描述内容:">
              <quillEditor class="quill-editor"
              v-model="formItem.content"
                :content="formItem.content"
              >
              </quillEditor>
            </FormItem>
            <br>
                  </Col>
                </Row>
                <Row>
                  <Col span="16">
                    <FormItem label="指定审核人:">
                      <Select v-model="formItem.assigned" prefix="md-person" filterable multiple>
                        <Option v-for="i in this.assigned_choicelist" :value="i.value" :key="i.label">{{i.label}}</Option>
                      </Select>
                    </FormItem>
                  </Col>
                </Row>
                <Row>
                  <Col span="16">
                    <FormItem label="添加抄送人:">
                      <Select v-model="formItem.copyuser" prefix="ios-person-add-outline" filterable multiple>
                        <Option v-for="i in this.assigned_choicelist" :value="i.value" :key="i.label">{{i.label}}</Option>
                      </Select>
                    </FormItem>
                  </Col>
                </Row>
                <FormItem>
                  <!--<Button type="warning" icon="android-search" @click.native="test_sql()">重置</Button>-->
                  <Button v-if="methodsvalue === 'post'" type="success" icon="ios-redo" @click.native="commitorder()" style="margin-left: 1%">提交</Button>
                </FormItem>
              </Form>
            </div>
          </div>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
/* eslint-disable */
// eslint-disable-next-line
import { quillEditor } from 'vue-quill-editor'
import axios from 'axios'
    export default {
      name: 'board',
      components: {
      quillEditor
    },
        data () {
            return {
              methodsvalue: ''
            }
        },
        props: {
          assigned_choicelist: {
      type: Array,
      default: []
    },
    formItem: {
      type: Object,
      default: {}
    },
    content: {
      type: String,
      default: ''
    },
    methodsvalue: {
      type: String,
      default: ''
    }
  },
  methods: {
  },
    }
</script>
