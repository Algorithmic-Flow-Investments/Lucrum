import * as requests from "@/helpers/requests"

export default class Target {
	constructor(data) {
		this.unpack(data);
		this.fetched = false
	}

	unpack(data) {
		this.id = data.id;
		this.name = data.name || "";
		this.is_internal = data.is_internal || false;
		this.tag_ids = data.tag_ids || [];
		this.usages = data.usages || 0;
		this.strings = data.strings || [];
	}

	fetch() {
		return new Promise((resolve, reject) => {
			if (!this.id) reject();
			requests.get(`targets/get/${this.id}`).then(data => {
				this.fetched = true
				this.unpack(data)
				resolve()
			})
		})
	}

	clone() {
		return new Target(this)
	}

	toJSON() {
		return {
			id: this.id,
			name: this.name,
			is_internal: this.is_internal,
			tag_ids: this.tag_ids,
			strings: this.strings
		}
	}

	commit() {
		return new Promise((resolve, reject) => {
			if (this.id) {
				requests.post(`targets/update/${this.id}`, this).then(data => {
					this.unpack(data)
					resolve()
				}).catch(exception => reject(exception))
			} else {
				requests.post(`targets/add`, this).then(() => resolve()).catch(exception => reject(exception))
			}
		})
	}

	delete() {
		requests.del(`targets/delete/${this.id}`)
	}
}
