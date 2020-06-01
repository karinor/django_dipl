const defaultMapClasses = {
    contacts: ".contacts-block__map-container",
    order: ".checkout-form__map-container"
}

class YMap {
    /**
     * Яндекс карта
     * @param {HTMLElement} container Контейнер с метками
     */
    constructor(container) {
        if (!container || container === null) return null

        this.container = container
        this.propPlacemarks = new Array()
        this.map = null

        // Получение свойств меток карты
        Array.prototype.slice.call(container.children).forEach((HTMLPlacemark) => {
            this.propPlacemarks.push({
                lat: HTMLPlacemark.dataset.lat.replace(/,/, '.'),
                lng: HTMLPlacemark.dataset.lng.replace(/,/, '.'),
                popup: HTMLPlacemark.dataset.popup,
                message: HTMLPlacemark.dataset.message
            })
            HTMLPlacemark.remove()
        })

        // Создание карты
        this.map = new ymaps.Map(container, {
            center: [this.propPlacemarks[0].lat, this.propPlacemarks[0].lng],
            zoom: 16,
            controls: [],
        }, {
            searchControlProvider: 'yandex#search'
        })

        // Создание и добавление макреров на карту
        Array.prototype.slice.call( this.propPlacemarks ).forEach((props) => {
			this.addPlacemark(props)
		})

        // Перецентровка после изменения размера карты
        this.map.events.add('sizechange', () => {
            this.map.setBounds(this.map.geoObjects.getBounds(), {checkZoomRange: true})
        })

        this.container.ymap = this
    }

    /**
     * Добавление метки на карту
     * @param {{lat: string, lng: string, popup?: string, message?: string}} props Свойства метки
     */
    addPlacemark(props) {
        const placemark = new ymaps.Placemark([props.lat, props.lng], {
            hintContent: props.message,
            balloonContent: props.popup,
        })
        this.map.geoObjects.add(placemark)
        return placemark
    }
}

if (window.ymaps !== undefined)
    ymaps.ready(function () {
        Array.prototype.slice.call( document.querySelectorAll(defaultMapClasses.contacts) ).forEach(function(container) {
			new YMap(container)
		})
        Array.prototype.slice.call( document.querySelectorAll(defaultMapClasses.order) ).forEach(function(container) {
			new YMap(container)
		})
    })


/////////////
//   API   //
/////////////

window.YMap = YMap