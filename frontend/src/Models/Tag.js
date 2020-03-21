import store from "@/store";
import * as requests from "@/helpers/requests";

export default class Tag {
	constructor(data) {
		this.unpack(data);
	}

	unpack(data) {
		this.id = data.id;
		this.name = data.name || "";
		this.category_id = data.category_id || null;
		this.category = this.getCategory()
	}

	getCategory() {
		let data = store.state.categories
		if (this.category_id === null) {
			return null
		}
		return data.filter(c => c.id === this.category_id)[0]
	}

	toJSON() {
		return {
			id: this.id,
			name: this.name,
			category_id: this.category_id
		}
	}

	commit() {
		return new Promise((resolve, reject) => {
			if (this.id) {
				requests.post(`tags/update/${this.id}`, this).then(data => {
					this.unpack(data)
					resolve()
				}).catch(exception => reject(exception))
			} else {
				requests.post(`tags/add`, this).then(() => resolve()).catch(exception => reject(exception))
			}
		})
	}

	delete() {
		requests.del(`tags/delete/${this.id}`)
	}
}
