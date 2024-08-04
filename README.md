# Marketplace Integration Django Project

Bu proje, IKAS ve Hepsiburada gibi birden fazla marketplace için API entegrasyonu sağlayan bir Django uygulamasıdır. Bu entegrasyonlar aracılığıyla farklı kanallardan gelen siparişler proje veritabanına kaydedilir.



## Akış

mp-integration/shop/channels içerisinde her markanın kendi integration, command, task yapıları oluşturulmuştur. Bu yapıda her Market Place için gereksinimlere göre özelleştirmeler bulunmaktadır. Opsiyonel olarak genişletilebilir ve geliştirilebilir esnek bir yapıda kullanılmasına özen gösterilmiştir.



1. Celery Beat ile belirtilen zaman aralığında ilgili task `get_orders_cron` tetiklenir.
2. Tetiklenen bu task, ilgili Integration instance'ının `do_action` metodunu çağırır.
3. `do_action` metodu, aldığı parametreler ile ilgili `Command` sınıfını çağırır.
4. Bu command sınıfı, istenilen action'ın operasyon sürecini yönetir.

Bu akış, entegrasyon sürecinin otomatik ve düzenli bir şekilde gerçekleşmesini sağlar. Her bir adım, belirli bir görevi yerine getirir ve bir sonraki adıma geçer. Bu yapı, farklı marketplace'ler için özelleştirilebilir ve genişletilebilir bir entegrasyon süreci sunar.

