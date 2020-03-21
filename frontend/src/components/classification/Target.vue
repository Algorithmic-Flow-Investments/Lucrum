<template>
	<div class="segment">
		<div class="main">{{ target.name }} <b-tag>Usages: {{target.usages}}</b-tag> <b-tag type="is-danger" class="is-clickable" @click.native="$emit('delete')">Delete</b-tag></div>
		<b-taglist>
			<b-tag type="is-primary" @click.native="startSelecting()" class="is-clickable">Add tag</b-tag>
			<b-tag type="is-info" v-for="tagId in target.tag_ids" :key="tagId" closable
				   @close="removeTag(tagId)">{{getTag(tagId).name}}</b-tag>
		</b-taglist>


		<b-modal :active.sync="selectingTag" has-modal-card>
			<div class="modal-card" style="width: auto">
				<header class="modal-card-head">
					<p class="modal-card-title">Select tags for {{target.name}}</p>
					<b-field>
						<b-input placeholder="Search..."
								 type="search"
								 icon="magnify"
								 ref="search"
								 v-model="search">
						</b-input>
					</b-field>
				</header>
				<section class="modal-card-body flex-container">
					<div v-for="tag in searched_tags" :key="tag.id" class="tag-item" :class="{selected: selectedTags.filter(t => t === tag.id).length}" @click="selectTag(tag)">
						<b-icon icon="tag" type="is-medium"></b-icon>
						<div class="sub" v-if="tag.category">{{ tag.category.name}}</div>
						<div class="name">{{ tag.name }}</div>
					</div>
				</section>
				<footer class="modal-card-foot">
					<b-button type="is-primary" :loading="sending" @click="submit">Save</b-button>
					<button class="button" type="button" @click="selectingTag=false">Cancel</button>
				</footer>
			</div>
		</b-modal>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests";

	export default {
		name: "Target",
		props: ['target'],
		data() {
			return {
				selectingTag: false,
				selectedTags: [],
				sending: false,
				tags: this.l_tags,
				search: ""
			}
		},
		computed: {
			searched_tags() {
				if (this.search === "") {
					return this.l_tags
				}
				return this.l_tags.filter(tag => {
					return tag.name.toLowerCase().includes(this.search.toLowerCase()) ||
						   (tag.category && tag.category.name.toLowerCase().includes(this.search.toLowerCase()));
				})
			}
		},
		methods: {
			getTag(tagId) {
				if (!tagId) {
					return null
				}
				return this.l_tags.filter(tag => tag.id === parseInt(tagId))[0]
			},
			startSelecting() {
				this.selectingTag = true;
				this.selectedTags = [...this.target.tag_ids]
				this.$nextTick(() => this.$refs.search.focus())
			},
			selectTag(tag){
				if (this.selectedTags.filter(t => t === tag.id).length){
					this.selectedTags.splice(this.selectedTags.indexOf(tag.id), 1);
				}
				else {
					this.selectedTags.push(tag.id)
				}
			},
			removeTag(tag){
				this.selectedTags = this.target.tag_ids.filter(item => item !== tag)
				this.submit()
			},
			submit(){
				let _submit = () => {
					this.selectingTag = false
					this.target.tag_ids = [...this.selectedTags]
					this.target.commit()
				}
				if (!this.target.fetched) {
					this.target.fetch().then(() => _submit())
				}
				else {
					_submit()
				}
			}
		}
	};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";

	/deep/ .tags:not(:last-child) {
		margin-bottom: -0.5rem !important;
	}

	.flex-container {
		display: flex;
		flex-wrap: wrap;
		height: auto;
	}

	.tag-item {
		/*font-size: 20px;*/
		margin: 5px;
		background-color: $primary;
		color: nth($greens, 1);
		width: 100px;
		height: 100px;
		text-align: center;
		line-height: 50px;
		padding: 5px;
		cursor: pointer;
		border-radius: 4px;
		flex-shrink: 0;
		position: relative;
	}

	.tag-item .icon {
		width: 100%;
	}

	.tag-item .sub {
		font-size: 14px;
		line-height: normal;
		/*position: absolute;*/
		/*left: 50%;*/
		/*transform: translate(-50%, -10%);
		padding-bottom: 10px;*/
	}

	.tag-item .name {
		line-height: normal;
		font-size: 20px;
	}
	.tag-item.selected {
		background-color: $secondary;
		color: $text-strong;
	}


	.segment {
		padding-bottom: 10px;
		padding-top: 10px;
		border-bottom: 1px solid #32333d;
	}

	.main {
		font-size: 24px;
		color: $text-strong;
		margin-bottom: 5px;
	}

</style>
