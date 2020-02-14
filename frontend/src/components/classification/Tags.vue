<template>
	<div class="sect flex-container">
			<div v-for="tag in l_tags" :key="tag.id">
				<div class="tag-item" @click="selectingCategory=tag">
					<b-icon icon="tag" type="is-medium"></b-icon>
					<div class="sub" v-if="tag.category">{{ tag.category.name}}</div>
					<div>{{ tag.name }}</div>
				</div>

				<b-modal :active="selectingCategory === tag" has-modal-card >
					<div class="modal-card" style="width: auto">
						<header class="modal-card-head">
							<p class="modal-card-title">Select category for {{tag.name}}</p>
						</header>
						<section class="modal-card-body flex-container">
							<div v-for="category in l_categories" :key="category.id" class="tag-item" :class="{selected: tag.category !== null && tag.category.id === category.id}" @click="submit(tag, category)">
								<b-icon icon="tag" type="is-medium"></b-icon>
								<div>{{ category.name }}</div>
							</div>

						</section>
						<footer class="modal-card-foot">
							<button class="button" type="button" @click.stop="selectingCategory=false">Cancel</button>
						</footer>
					</div>
				</b-modal>
			</div>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests";

	export default {
		name: "Tags",
		data () {
			return {
				selectingCategory: false,
			}
		},
		methods: {
			submit(tag, category) {
				tag.category_id = category.id
				this.selectingCategory = false
				tag.commit()
			}
		}
	};
</script>

<style scoped lang="scss">
	@import "~@/assets/colours";

	.flex-container {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		height: auto;
	}

	.tag-item {
		font-size: 24px;
		margin: 5px;
		background-color: $primary;
		color: nth($greens, 1);
		width: 120px;
		height: 120px;
		text-align: center;
		line-height: 60px;
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
		font-size: 16px;
		line-height: normal;
		position: absolute;
		left: 50%;
		transform: translate(-50%, -10%);
		padding-bottom: 10px;
	}

	.tag-item.selected {
		background-color: $secondary;
		color: $text-strong;
	}

</style>
