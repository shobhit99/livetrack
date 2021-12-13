 # if linebreak in packet
        if b'\r\n' in data:
            # split packet
            tempbuf = data.split(b'\r\n')
            for i in tempbuf:
                if i == b'':
                    continue
                if tempbuf[-1] == b'':
                    if self.packet != b'':
                        self.packet += i
                        self.packet = self.packet.decode("utf-8")
                        buf = self.packet.split("@")
                        lenoflen = len(str(buf[0]))
                        sometemp = self.packet[lenoflen+1:]
                        try:
                            cmd = eval(sometemp)
                        except:
                            print(self.packet)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
                    elif self.packet == b'':
                        self.packet = i
                        self.packet = self.packet.decode("utf-8")
                        buf = self.packet.split("@")
                        lenoflen = len(str(buf[0]))
                        sometemp = self.packet[lenoflen+1:]
                        cmd = eval(sometemp)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
                else:
                    if tempbuf.index(i) == len(tempbuf)-1:
                        self.packet += i
                    elif self.packet != b'':
                        self.packet += i
                        self.packet = self.packet.decode("utf-8")
                        buf = self.packet.split("@")
                        lenoflen = len(str(buf[0]))
                        sometemp = self.packet[lenoflen+1:]
                        cmd = eval(sometemp)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
                    elif self.packet == b'':
                        self.packet = i
                        self.packet = self.packet.decode("utf-8")
                        buf = self.packet.split("@")
                        lenoflen = len(str(buf[0]))
                        sometemp = self.packet[lenoflen+1:]
                        cmd = eval(sometemp)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
        else:
            # start of frame sent i.e 655536 bytes
            self.packet += data