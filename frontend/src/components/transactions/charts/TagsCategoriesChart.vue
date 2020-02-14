<template>
	<donut :value="pie" @click="setTagCat">
		<div slot="default">
			<div>{{totalType | capitalize}}</div>
			<br/>
			<div class="money">{{ '£' + Math.round(tweenTotal) }}</div>
			<br/>
			<total-type-toggle @changed="setTotalType"></total-type-toggle>
			<br/>
		</div>
		<div ref="selected" slot="tooltip" slot-scope="selected">
			<div>{{(selected.child !== null) ? getTag(selected.child).name : getCategory(selected.parent).name}}</div>
			<br/>
			<div class="money">{{ '£' + ((selected.child !== null) ? Math.round(getTag(selected.child).total[totalType]) : Math.round(getCategory(selected.parent).total[totalType]))}}</div>
			<br/>
			<total-type-toggle @changed="setTotalType"></total-type-toggle>
			<br/>
		</div>
	</donut>
</template>

<script>
	import Donut, { DonutSegment } from "@/components/charts/Donut";
	import TotalTypeToggle from "@/components/transactions/charts/TotalTypeToggle";

	export default {
		name: "TagsCategoriesChart",
		components: { TotalTypeToggle, Donut },
		props: ['stats', 'chart'],
		data() {
			return {
				tweenTotal: this.total || 0,
				totalType: null
			}
		},
		watch: {
			'total': function() {
				let jump = (this.total - this.tweenTotal) / 30
				let tween = setInterval(() => {
					if (Math.abs(this.tweenTotal - this.total) < 16) {
						this.tweenTotal = this.total
						clearInterval(tween)
						return
					}
					this.tweenTotal += jump
				}, 10)
			}
		},
		methods: {
			getTag(tagId) {
				if (!tagId || tagId === -1) {
					return null
				}
				let tag = this.l_tags.filter(tag => tag.id === parseInt(tagId))[0]
				let cat_id = tag.category_id || -1
				tag.total = this.chart[cat_id].tags[tagId]
				return tag
			},
			getCategory(catId) {
				let category;
				if (parseInt(catId) === -1) {
					category = {name: "Misc", id: -1}
					catId = -1
				}
				else {
					category = this.l_categories.filter(cat => cat.id === parseInt(catId))[0]
				}
				category.total = this.chart[catId].total
				return category
			},
			setTagCat(selected){
				if (!selected) {
					this.$emit('tagcat', {cat_id: null, tag_id: null})
				}
				else {
					this.$emit('tagcat', {cat_id: selected.parent, tag_id: selected.child})
				}
			},
			setTotalType(selected){
				this.$emit('totaltype', selected)
				this.totalType = selected
			},
			getPie (totalType, colour1, colour2) {
				return Object.keys(this.chart).map(key => {
					let value = this.chart[key].total[totalType]
					let children = Object.keys(this.chart[key].tags).map(tag_key => {
						let value = this.chart[key].tags[tag_key][totalType]
						return new DonutSegment(this.getTag(tag_key), Math.abs(value), colour1, [])
					}).filter(item => item !== null)
					return new DonutSegment(this.getCategory(key), Math.abs(value), colour2, children)
				}).filter(item => item !== null)
			}
		},
		computed: {
			pie () {
				if (this.chart === {} || !this.totalType || !this.l_tags) return [];
				if (this.totalType === 'gross') {
					let p = this.getPie('outgoing', 'outgoing', 'outgoing')
					p.push(...this.getPie('income', 'income', 'income'))
					return p
				}
				return this.getPie(this.totalType, 'tag', 'category')
			},
			total() {
				if (!this.stats) return 0
				switch (this.totalType) {
					case 'outgoing':
						return this.stats.total.outgoing
					case 'gross':
						return this.stats.total.gross
					case 'income':
						return this.stats.total.income
				}
				return 0
			}
		},
		filters: {
			capitalize: function (value) {
				if (!value) return ''
				value = value.toString()
				return value.charAt(0).toUpperCase() + value.slice(1)
			}
		}
	};
</script>

<style scoped lang="scss">
	@import "../../../assets/colours";

	.money {
		font-size: 3em;
		color: white;
	}

	/deep/ .tag {
		fill: $secondary;
	}

	/deep/ .category {
		fill: $primary;
	}

	/deep/ .income {
		fill: $yellow;
	}

	/deep/ .outgoing {
		fill: $red;
	}

</style>
