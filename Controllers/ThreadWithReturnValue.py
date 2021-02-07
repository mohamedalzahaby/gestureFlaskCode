from threading import Thread

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return



# twrv1 = ThreadWithReturnValue(target=read_model, args=("mysite/SVM_Model.sav",))
# twrv2 = ThreadWithReturnValue(target=get_Test_img_csv, args=(image_path,))
# twrv1.start()
# twrv2.start()
# model = twrv1.join()
# Test_img_csv = twrv2.join()